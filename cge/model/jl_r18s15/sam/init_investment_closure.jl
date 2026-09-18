# Explicit closure extension. Walras remains a reported accounting diagnostic.
@variables m begin
    ptinv_idx[r=Regions] >= 0.000001, (start=ptinv0[r])
end
@NLparameters m begin
    foreign_saving_target[r=Regions] == save0[r]
end
function eq_investment_closure()
    @mapping(m, eq_external_closure[r in setdiff(Regions,[2])], save[r]-foreign_saving_target[r])
    @complementarity(m, eq_external_closure, ptinv_idx[setdiff(Regions,[2])])
    @mapping(m, eq_global_numeraire, ptinv_idx[2]-ptinv0[2])
    @complementarity(m, eq_global_numeraire, ptinv_idx[2])
end
