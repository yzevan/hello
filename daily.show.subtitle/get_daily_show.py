import os,sys
id = 171
maxid = 180
while id <= maxid:
	id_str = '%0*d' % (3, id)
	os.system("wget 'http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_17/episode_" + id_str + "/ds_17" + id_str +"_act1.dfxp.xml'")
	os.system("wget 'http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_17/episode_" + id_str + "/ds_17" + id_str +"_act2.dfxp.xml'")
	os.system("wget 'http://a1.akadl.mtvnservices.com/9950/mtvnorigin/gsp.comedystor/com/dailyshow/TDS/season_17/episode_" + id_str + "/ds_17" + id_str +"_act3.dfxp.xml'")
	id += 1
	
	
