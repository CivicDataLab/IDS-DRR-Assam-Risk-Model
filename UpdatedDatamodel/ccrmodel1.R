
library(ggcorrplot)
library(FactoMineR)
library(caret)
library(deaR)
library(BAMMtools)

socioeconomic <- read.csv("F:/OneDrive - IIT Hyderabad/MASTER_VARIABLES.csv")
var_interest = c("object_id","Total_Animal_Affected","Population_affected_Total",
                 "Crop_Area","Total_House_Fully_Damaged","Embankments.affected",
                 "Roads","Bridge","Relief_Camp_inmates",
                 "mean_sexratio","sum_aged_population",
                 "schools_count","health_centres_count","rail_length",
                 "road_length","Embankment.breached","net_sown_area_in_hac","avg_electricity",
                 "rc_nosanitation_hhds_pct","rc_piped_hhds_pct",
                 "cum_CIDF_tenders_awarded_value","cum_RIDF_tenders_awarded_value",
                 "cum_SDRF_tenders_awarded_value","cum_SOPD_tenders_awarded_value")
data_interest = socioeconomic[var_interest]

prepoc <- preProcess(as.data.frame(data_interest),method = c("range"))
data_scaled <-predict(prepoc,as.data.frame(data_interest))
data_scaled['schools_count'] = 1 - data_scaled['schools_count']
data_scaled['health_centres_count'] = 1 - data_scaled['health_centres_count']
data_scaled['rail_length'] = 1 - data_scaled['rail_length']
data_scaled['road_length'] = 1 - data_scaled['road_length']
data_scaled['avg_electricity'] = 1 - data_scaled['avg_electricity']
data_scaled['rc_piped_hhds_pct'] = 1 - data_scaled['rc_piped_hhds_pct']
data_scaled['reverse_popdam'] = 1 - data_scaled['Population_affected_Total']
data_scaled['reverse_animal'] = 1 - data_scaled['Total_Animal_Affected']
data_scaled['reverse_crop'] = 1 - data_scaled['Crop_Area']
data_scaled['reverse_house'] = 1 - data_scaled['Total_House_Fully_Damaged']
data_scaled['reverse_embankment'] = 1 - data_scaled['Embankments.affected']
data_scaled['reverse_road'] = 1 - data_scaled['Roads']
data_scaled['reverse_bridge'] = 1 - data_scaled['Bridge']
data_scaled['reverse_SOPD'] = 1 - data_scaled['cum_SOPD_tenders_awarded_value']
data_scaled['reverse_SDRF'] = 1 - data_scaled['cum_SDRF_tenders_awarded_value']
data_scaled['reverse_RIDF'] = 1 - data_scaled['cum_RIDF_tenders_awarded_value']
data_scaled['reverse_CIDF'] = 1 - data_scaled['cum_CIDF_tenders_awarded_value']
data_scaled['dummy_output'] = 1

ccr_model <-read_data(data_scaled,ni = 4,no = 7,dmus = 1, inputs = 32:35, outputs =  25:31)
result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1:180,dmu_ref = 1:180)
eff <- efficiencies(result_ccr)
j <- getJenksBreaks(eff,5)
eff_combined <-eff

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 181:360,dmu_ref = 181:360)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 361:540,dmu_ref = 361:540)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 541:720,dmu_ref = 541:720)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 721:900,dmu_ref = 721:900)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 901:1080,dmu_ref = 901:1080)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1081:1260,dmu_ref = 1081:1260)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1261:1440,dmu_ref = 1261:1440)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1441:1620,dmu_ref = 1441:1620)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1621:1800,dmu_ref = 1621:1800)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1801:1980,dmu_ref = 1801:1980)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1981:2160,dmu_ref = 1981:2160)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2161:2340,dmu_ref = 2161:2340)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2341:2520,dmu_ref = 2341:2520)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2521:2700,dmu_ref = 2521:2700)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2701:2880,dmu_ref = 2701:2880)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2881:3060,dmu_ref = 2881:3060)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3061:3240,dmu_ref = 3061:3240)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3241:3420,dmu_ref = 3241:3420)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3421:3600,dmu_ref = 3421:3600)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3601:3780,dmu_ref = 3601:3780)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3781:3960,dmu_ref = 3781:3960)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3961:4140,dmu_ref = 3961:4140)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4141:4320,dmu_ref = 4141:4320)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4321:4500,dmu_ref = 4321:4500)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4501:4680,dmu_ref = 4501:4680)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4681:4860,dmu_ref = 4681:4860)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4861:5040,dmu_ref = 4861:5040)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)


result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 5041:5220,dmu_ref = 5041:5220)
eff <- efficiencies(result_ccr)
j <- rbind(j,getJenksBreaks(eff,5))
eff_combined <-cbind(eff_combined,eff)

write.csv(eff_combined,"efficiencies_dummy.csv")
write.csv(j,"jenksbreaks_tenders.csv")

ccr_model <-read_data(data_scaled,ni = 11,no = 7,dmus = 1, inputs = 10:20, outputs =  25:31)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1:180,dmu_ref = 1:180)
vul_eff <- efficiencies(result_ccr)
vul_j <- getJenksBreaks(vul_eff,5)
vul_eff_combined <-vul_eff

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 181:360,dmu_ref = 181:360)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 361:540,dmu_ref = 361:540)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 541:720,dmu_ref = 541:720)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 721:900,dmu_ref = 721:900)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 901:1080,dmu_ref = 901:1080)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1081:1260,dmu_ref = 1081:1260)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1261:1440,dmu_ref = 1261:1440)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1441:1620,dmu_ref = 1441:1620)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1621:1800,dmu_ref = 1621:1800)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1801:1980,dmu_ref = 1801:1980)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 1981:2160,dmu_ref = 1981:2160)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2161:2340,dmu_ref = 2161:2340)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2341:2520,dmu_ref = 2341:2520)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2521:2700,dmu_ref = 2521:2700)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2701:2880,dmu_ref = 2701:2880)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 2881:3060,dmu_ref = 2881:3060)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3061:3240,dmu_ref = 3061:3240)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3241:3420,dmu_ref = 3241:3420)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3421:3600,dmu_ref = 3421:3600)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3601:3780,dmu_ref = 3601:3780)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3781:3960,dmu_ref = 3781:3960)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 3961:4140,dmu_ref = 3961:4140)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4141:4320,dmu_ref = 4141:4320)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4321:4500,dmu_ref = 4321:4500)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4501:4680,dmu_ref = 4501:4680)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4681:4860,dmu_ref = 4681:4860)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 4861:5040,dmu_ref = 4861:5040)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)


result_ccr <- model_sbmeff(ccr_model,orientation = "io",rts  ="crs",dmu_eval = 5041:5220,dmu_ref = 5041:5220)
vul_eff <- efficiencies(result_ccr)
vul_j <- rbind(vul_j,getJenksBreaks(vul_eff,5))
vul_eff_combined <-cbind(vul_eff_combined,vul_eff)

write.csv(vul_eff_combined,"efficiencies_vulnerabilities.csv")
write.csv(vul_j,"jenksbreaks_vu.csv")





