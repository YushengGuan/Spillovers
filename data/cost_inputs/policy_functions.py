@lru_cache(None)
def rate(tech, receiver, supplier, year):
    if receiver == supplier:
        return 0.0
    d = tariff[tech]
    if receiver == 'GBR':
        d = d[d.year.ge(2021) if year >= 2021 else d.year.le(2020)]
    z = d[d.importer_iso3.eq(receiver) & d.supplier_iso3.eq(supplier)]
    exact = z[z.year.eq(year)]
    if len(exact):
        value = float(exact.applied_rate_pct.iloc[0]) / 100
        status = 'observed_bilateral_or_MFN'
        anchor = year
    elif len(z):
        q = z.loc[(z.year - year).abs().idxmin()]
        value = float(q.applied_rate_pct) / 100
        anchor = int(q.year)
        status = 'nearest_source_year_within_UK_regime'
    else:
        q = d[d.importer_iso3.eq(receiver) & d.mfn_rate_pct.notna()]
        if len(q):
            yr = int(q.loc[(q.year - year).abs().idxmin(), 'year'])
            value = float(q[q.year.eq(yr)].mfn_rate_pct.median()) / 100
            anchor = yr
            status = 'reporter_MFN_fallback'
        else:
            if tech == 'wind':
                q = wind[wind.iso3.eq(receiver) & wind.year.eq(year)]
                value = float(q.tariff_alt_regular.iloc[0]) if len(q) else 0.0
            else:
                q = per[per.iso3.eq(receiver) & per.year.eq(year)]
                value = float(np.average(q.regular_alt, weights=q.weight)) if len(q) else 0.0
            anchor = year
            status = 'inherited_alternative_rate_or_zero_assumption'
    assert np.isfinite(value) and value >= 0
    tariff_ledger.append(dict(technology=tech, iso3=receiver, supplier=supplier, year=year, rate=value, status=status, source_year=anchor, uses_future_year=anchor > year))
    return value

def border(tech, receiver, year, suppliers, price_kw, actual_policy):
    yr = year if actual_policy else 2010
    duty = np.array([rate(tech, receiver, x, yr) for x in suppliers])
    rent = np.zeros(len(suppliers))
    if receiver == 'CHN':
        return (duty, rent)
    j = suppliers.index('CHN')
    if tech == 'wind':
        q = windpol.loc[receiver, yr]
        duty[j] = float(q.tariff_cn_effective)
    else:
        z = periods[receiver, yr]
        w = z.weight.to_numpy()
        ckkey = None
        price = price_kw[j] / 1000
        base = z.regular_cn.to_numpy() + z.coverage.to_numpy() * (z.common_rate.to_numpy() + z.cn_extra.to_numpy())
        cap = z.eu_ad_cap.to_numpy()
        gap = np.maximum(z.eu_floor.to_numpy() / price - 1, 0)
        share = z.eu_compliant_share.to_numpy() * z.coverage.to_numpy()
        u = z.eu_branch.eq('undertaking').to_numpy()
        v = z.eu_branch.eq('variable_MIP_duty').to_numpy()
        dcn = base + np.where(u, (1 - share) * cap, 0) + np.where(v, share * np.minimum(gap, cap) + (1 - share) * cap, 0)
        duty[j] = np.dot(w, dcn)
        rent[j] = np.dot(w, np.where(u, share * gap, 0))
        common = float(np.dot(w, z.common_rate * z.coverage))
        for k, supplier in enumerate(suppliers):
            if supplier not in [receiver, 'CHN']:
                duty[k] += common
    for k, supplier in enumerate(suppliers):
        if supplier == receiver:
            duty[k] = 0
            rent[k] = 0
    return (duty, rent)