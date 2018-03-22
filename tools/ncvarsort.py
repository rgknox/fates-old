from netCDF4 import Dataset
import numpy
import filemod

# program sorts the variables based on the provided list, and pulls them one at a time from an existing file and adds them to a new file in the sorted order.
# based on code here: https://gist.github.com/guziy/8543562

# if variable names are changed, will need to reconstruct this list.
var_list = ['fates_history_ageclass_bin_edges','fates_history_height_bin_edges','fates_history_sizeclass_bin_edges','fates_base_mr_20','fates_bbopt_c3','fates_bbopt_c4','fates_canopy_closure_thresh','fates_cohort_fusion_tol','fates_comp_excln','fates_cwd_fcel','fates_cwd_flig','fates_hydr_psi0','fates_hydr_psicap','fates_init_litter','fates_logging_coll_under_frac','fates_logging_collateral_frac','fates_logging_dbhmax_infra','fates_logging_dbhmin','fates_logging_direct_frac','fates_logging_event_code','fates_logging_mechanical_frac','fates_mort_disturb_frac','fates_nignitions','fates_patch_fusion_tol','fates_phen_a','fates_phen_b','fates_phen_c','fates_phen_chiltemp','fates_phen_coldtemp','fates_phen_doff_time','fates_phen_drought_threshold','fates_phen_mindayson','fates_phen_ncolddayslim','fates_stress_mort','fates_understorey_death','fates_allom_agb_frac','fates_allom_agb1','fates_allom_agb2','fates_allom_agb3','fates_allom_agb4','fates_allom_amode','fates_allom_blca_expnt_diff','fates_allom_cmode','fates_allom_d2bl1','fates_allom_d2bl2','fates_allom_d2bl3','fates_allom_d2ca_coefficient_max','fates_allom_d2ca_coefficient_min','fates_allom_d2h1','fates_allom_d2h2','fates_allom_d2h3','fates_allom_dbh_maxheight','fates_allom_fmode','fates_allom_hmode','fates_allom_l2fr','fates_allom_latosa_int','fates_allom_latosa_slp','fates_allom_lmode','fates_allom_sai_scaler','fates_allom_smode','fates_allom_stmode','fates_alpha_SH','fates_bark_scaler','fates_BB_slope','fates_bmort','fates_branch_turnover','fates_c2b','fates_c3psn','fates_clumping_index','fates_crown_depth_frac','fates_crown_kill','fates_cushion','fates_dbh_repro_threshold','fates_displar','fates_dleaf','fates_evergreen','fates_fr_fcel','fates_fr_flab','fates_fr_flig','fates_freezetol','fates_froot_leaf','fates_frootcn','fates_germination_timescale','fates_grperc','fates_hf_sm_threshold','fates_hgt_min','fates_hydr_avuln_gs','fates_hydr_avuln_node','fates_hydr_epsil_node','fates_hydr_fcap_node','fates_hydr_kmax_node','fates_hydr_p_taper','fates_hydr_p50_gs','fates_hydr_p50_node','fates_hydr_pinot_node','fates_hydr_pitlp_node','fates_hydr_resid_node','fates_hydr_rfrac_stem','fates_hydr_rs2','fates_hydr_srl','fates_hydr_thetas_node','fates_initd','fates_jmaxha','fates_jmaxhd','fates_jmaxse','fates_leaf_long','fates_leaf_stor_priority','fates_leafcn','fates_lf_fcel','fates_lf_flab','fates_lf_flig','fates_maintresp_reduction_curvature','fates_maintresp_reduction_intercept','fates_pft_used','fates_prescribed_mortality_canopy','fates_prescribed_mortality_understory','fates_prescribed_npp_canopy','fates_prescribed_npp_understory','fates_prescribed_recruitment','fates_rholnir','fates_rholvis','fates_rhosnir','fates_rhosvis','fates_root_long','fates_roota_par','fates_rootb_par','fates_rootprof_beta','fates_season_decid','fates_seed_alloc','fates_seed_alloc_mature','fates_seed_decay_turnover','fates_seed_rain','fates_slatop','fates_smpsc','fates_smpso','fates_stress_decid','fates_taulnir','fates_taulvis','fates_tausnir','fates_tausvis','fates_tpuha','fates_tpuhd','fates_tpuse','fates_trim_inc','fates_trim_limit','fates_vcmax25top','fates_vcmaxha','fates_vcmaxhd','fates_vcmaxse','fates_wood_density','fates_woody','fates_xl','fates_z0mr','fates_alpha_FMC','fates_FBD','fates_low_moisture_Coeff','fates_low_moisture_Slope','fates_max_decomp','fates_mid_moisture','fates_mid_moisture_Coeff','fates_mid_moisture_Slope','fates_min_moisture','fates_SAV','fates_CWD_frac','fates_durat_slope','fates_fdi_a','fates_fdi_alpha','fates_fdi_b','fates_fire_wind_max','fates_fuel_energy','fates_max_durat','fates_miner_damp','fates_miner_total','fates_part_dens']

### modify the paths below to point to the new and old file names
fnamein = 'fates_params_default.nc'
fnameout = 'fates_params_default_sorted.nc'

dsin = Dataset(fnamein)
filemod.clobber(fnameout)
dsout = Dataset(fnameout,  "w", format="NETCDF3_CLASSIC")

#Copy dimensions
for dname, the_dim in dsin.dimensions.iteritems():
    print dname, len(the_dim)
    dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)


for i in range(len(var_list)):
    v_name = var_list[i]
    varin = dsin.variables[v_name]
    outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)
    print varin.datatype
    
    # Copy variable attributes
    outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
    
    outVar[:] = varin[:]


    # close the output file
dsout.close()
