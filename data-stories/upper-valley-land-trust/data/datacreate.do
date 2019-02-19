/******************************************
*******************************************
*** Data create file for UVLT Data ********
*******************************************
*******************************************/

cd "E:\Dartmouth\Statistics\WINTER 19\SIP\UVLT Raw Data"

log using "datacreatemerge.log", replace

import excel using "UVLTDataAnalysis.xls", firstrow



*Fix any issues with variables
drop FirstName LastName ZipCode City 

*Drop 19-20 variables because there are no donations for this fiscal year
drop U201920 R201920 V201920 E201920

*Label variables
label var ContactID "Respondent ID number" 
label var TownID "Unique ID number for Town of Residence" 
label var Town "Name of Town of Residence" 
label var State "State of Residence" 
label var LandOwnerTownID "Town ID for owned conserved land"
label var DeceasedDateYN "Respondent has died (1=yes)" 

gen DeceasedYear=year(DeceasedDate)
drop DeceasedDate
rename DeceasedYear DeceasedDate
label var DeceasedDate "Year of Death (for those who died)" 


label var U_Tot_Amt "Total Unrestricted Donation $,ALL YEARS" 
label var U_Tot_Cnt "Total Number of Unrestricted Donations, All YEARS" 

label var RTotAmt "Total Restricted Donation $,ALL YEARS" 
label var RTotCnt "Total Number of Restricted Donations, All YEARS" 
label var VTotCnt "Total Number of times R volunteered, ALL YEARS" 
label var ETotCnt "Total Number of UVLT Events Attended, ALL YEARS" 



label var U200001 "Total Unrestricted Donation $,2000-2001 Fiscal Year" 
label var U200102 "Total Unrestricted Donation $,2001-2002 Fiscal Year" 
label var U200203 "Total Unrestricted Donation $,2002-2003 Fiscal Year" 
label var U200304 "Total Unrestricted Donation $,2003-2004 Fiscal Year" 
label var U200405 "Total Unrestricted Donation $,2004-2005 Fiscal Year" 
label var U200506 "Total Unrestricted Donation $,2005-2006 Fiscal Year" 
label var U200607 "Total Unrestricted Donation $,2006-2007 Fiscal Year" 
label var U200708 "Total Unrestricted Donation $,2007-2008 Fiscal Year" 
label var U200809 "Total Unrestricted Donation $,2008-2009 Fiscal Year" 
label var U200910 "Total Unrestricted Donation $,2009-2010 Fiscal Year" 
label var U201011 "Total Unrestricted Donation $,2010-2011 Fiscal Year" 
label var U201112 "Total Unrestricted Donation $,2011-2012 Fiscal Year" 
label var U201213 "Total Unrestricted Donation $,2012-2013 Fiscal Year" 
label var U201314 "Total Unrestricted Donation $,2013-2014 Fiscal Year" 
label var U201415 "Total Unrestricted Donation $,2014-2015 Fiscal Year" 
label var U201516 "Total Unrestricted Donation $,2015-2016 Fiscal Year" 
label var U201617 "Total Unrestricted Donation $,2016-2017 Fiscal Year" 
label var U201718 "Total Unrestricted Donation $,2017-2018 Fiscal Year" 
label var U201819 "Total Unrestricted Donation $,2018-2019 Fiscal Year" 

label var R200001 "Total Restricted Donation $,2000-2001 Fiscal Year" 
label var R200102 "Total Restricted Donation $,2001-2002 Fiscal Year" 
label var R200203 "Total Restricted Donation $,2002-2003 Fiscal Year" 
label var R200304 "Total Restricted Donation $,2003-2004 Fiscal Year" 
label var R200405 "Total Restricted Donation $,2004-2005 Fiscal Year" 
label var R200506 "Total Restricted Donation $,2005-2006 Fiscal Year" 
label var R200607 "Total Restricted Donation $,2006-2007 Fiscal Year" 
label var R200708 "Total Restricted Donation $,2007-2008 Fiscal Year" 
label var R200809 "Total Restricted Donation $,2008-2009 Fiscal Year" 
label var R200910 "Total Restricted Donation $,2009-2010 Fiscal Year" 
label var R201011 "Total Restricted Donation $,2010-2011 Fiscal Year" 
label var R201112 "Total Restricted Donation $,2011-2012 Fiscal Year" 
label var R201213 "Total Restricted Donation $,2012-2013 Fiscal Year" 
label var R201314 "Total Restricted Donation $,2013-2014 Fiscal Year" 
label var R201415 "Total Restricted Donation $,2014-2015 Fiscal Year" 
label var R201516 "Total Restricted Donation $,2015-2016 Fiscal Year" 
label var R201617 "Total Restricted Donation $,2016-2017 Fiscal Year" 
label var R201718 "Total Restricted Donation $,2017-2018 Fiscal Year" 
label var R201819 "Total Restricted Donation $,2018-2019 Fiscal Year" 

label var V200001 "Number of Times Volunteered,2000-2001 Fiscal Year" 
label var V200102 "Number of Times Volunteered,2001-2002 Fiscal Year" 
label var V200203 "Number of Times Volunteered,2002-2003 Fiscal Year" 
label var V200304 "Number of Times Volunteered,2003-2004 Fiscal Year" 
label var V200405 "Number of Times Volunteered,2004-2005 Fiscal Year" 
label var V200506 "Number of Times Volunteered,2005-2006 Fiscal Year" 
label var V200607 "Number of Times Volunteered,2006-2007 Fiscal Year" 
label var V200708 "Number of Times Volunteered,2007-2008 Fiscal Year" 
label var V200809 "Number of Times Volunteered,2008-2009 Fiscal Year" 
label var V200910 "Number of Times Volunteered,2009-2010 Fiscal Year" 
label var V201011 "Number of Times Volunteered,2010-2011 Fiscal Year" 
label var V201112 "Number of Times Volunteered,2011-2012 Fiscal Year" 
label var V201213 "Number of Times Volunteered,2012-2013 Fiscal Year" 
label var V201314 "Number of Times Volunteered,2013-2014 Fiscal Year" 
label var V201415 "Number of Times Volunteered,2014-2015 Fiscal Year" 
label var V201516 "Number of Times Volunteered,2015-2016 Fiscal Year" 
label var V201617 "Number of Times Volunteered,2016-2017 Fiscal Year" 
label var V201718 "Number of Times Volunteered,2017-2018 Fiscal Year" 
label var V201819 "Number of Times Volunteered,2018-2019 Fiscal Year" 

label var E200001 "Number of UVLT Events Attended,2000-2001 Fiscal Year" 
label var E200102 "Number of UVLT Events Attended,2001-2002 Fiscal Year" 
label var E200203 "Number of UVLT Events Attended,2002-2003 Fiscal Year" 
label var E200304 "Number of UVLT Events Attended,2003-2004 Fiscal Year" 
label var E200405 "Number of UVLT Events Attended,2004-2005 Fiscal Year" 
label var E200506 "Number of UVLT Events Attended,2005-2006 Fiscal Year" 
label var E200607 "Number of UVLT Events Attended,2006-2007 Fiscal Year" 
label var E200708 "Number of UVLT Events Attended,2007-2008 Fiscal Year" 
label var E200809 "Number of UVLT Events Attended,2008-2009 Fiscal Year" 
label var E200910 "Number of UVLT Events Attended,2009-2010 Fiscal Year" 
label var E201011 "Number of UVLT Events Attended,2010-2011 Fiscal Year" 
label var E201112 "Number of UVLT Events Attended,2011-2012 Fiscal Year" 
label var E201213 "Number of UVLT Events Attended,2012-2013 Fiscal Year" 
label var E201314 "Number of UVLT Events Attended,2013-2014 Fiscal Year" 
label var E201415 "Number of UVLT Events Attended,2014-2015 Fiscal Year" 
label var E201516 "Number of UVLT Events Attended,2015-2016 Fiscal Year" 
label var E201617 "Number of UVLT Events Attended,2016-2017 Fiscal Year" 
label var E201718 "Number of UVLT Events Attended,2017-2018 Fiscal Year" 
label var E201819 "Number of UVLT Events Attended,2018-2019 Fiscal Year" 

*create new variables:


*1) Create Landowner dummy variable (1=respondent owns conserved land, 0=no)

gen ConservedOwner=1
replace ConservedOwner=0 if LandOwnerTownID==0 | LandOwnerTownID==. 
label var ConservedOwner "Respondent Owns Conserved Land (1=yes)" 


save "UVLTdata_individual.dta", replace 



*Create Community-Level Data Set
clear
import excel using "TownLevelData.xlsx", firstrow

*Label variables

label var TownID "Unique ID number for Town of Residence" 
label var Town "Name of Town of Residence" 
label var Nprojects "Number of UVLT Projects in Town (town-level)"
label var Nacres "Number of Acres owned by UVLT in Town (town-level)"
label var Nmembers "Number of UVLT donors in Town (town-level)"
label var MedianHHIncome "Median HH Income in Town (town-level), US Census"
label var MeanHHIncome "Mean HH Income in Town (town-level), US Census"
label var PercBAplus "% 4year College Graduates in Town (town-level), US Census"
label var PercAge55Plus "% Population Age55+ in Town (town-level), US Census"


save "TownLevelData.dta"



*Merge on community-level data
use "UVLTdata_individual.dta", clear

merge m:1 TownID using "TownLevelData.dta"

/*

    Result                           # of obs.
    -----------------------------------------
    not matched                         4,197
        from master                     4,190  (_merge==1)
        from using                          7  (_merge==2)

    matched                             9,737  (_merge==3)
    -----------------------------------------


*/
tab TownID if _merge==1
*towns not matched are all towns outside of the UV

tab TownID if _merge==2
*Seven UV towns not matched from using data..meaning we have nobody who lives in these towns in the data


drop _merge
save "UVLTdata_final.dta"




*Create community-level donation variables? 

 

*Wait until I hear back from Alison: Merge on Mailing list data (?)
*fix data/create needed variables
*label variables



*Save final data set

