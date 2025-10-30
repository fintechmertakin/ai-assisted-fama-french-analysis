log using "fama_french_analysis.txt", text replace


cd "D:\Dropbox\Dropbox\2025\PhD Admission\Courses and Lecture Notes\Fall 1\FINA6900\Week 3"



import delimited "F-F_Research_Data_5_Factors_2x3.csv", clear varnames(4) rowrange(5:749)

rename v1 date


gen str6 date_str = string(date)
gen year = real(substr(date_str, 1, 4))
gen month = real(substr(date_str, 5, 2))
gen date_monthly = ym(year, month)
format date_monthly %tm

drop date date_str year month
rename date_monthly date


save fama_french_5f_cleaned.dta, replace



gen year = year(dofm(date))
collapse (mean) mktrf smb hml rmw cma, by(year)

list year mktrf smb hml rmw cma, sep(0)

save fama_french_5f_annual_avg.dta, replace

use fama_french_5f_cleaned.dta, clear

tsset date
foreach var in mktrf smb hml rmw cma {
    tsline `var', title("`var' Over Time") xtitle("Date") ytitle("Return (%)") ///
    name(`var'_plot, replace)
}

sum mktrf smb hml rmw cma, detail

correlate mktrf smb hml rmw cma

pwcorr mktrf smb hml rmw cma, sig star(.05)


log close

