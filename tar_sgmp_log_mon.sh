#!/bin/sh

date_val=$1
mon_val=$2
mon_loop_val="0 1"
df_val="28"
file_prefix_val="Biz.Oss_JNRPE.log."
gz_val=".gz"
mon_loop_val_28="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28"
mon_loop_val_29="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29"
mon_loop_val_30="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30"
mon_loop_val_31="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31"
loop_val="00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23"

if [ "$mon_val" == "28" ]; then
	mon_loop_val=$mon_loop_val_28
	df_val="28"
elif [ "$mon_val" == "29" ]; then
	mon_loop_val=$mon_loop_val_29
	df_val="29"
elif [ "$mon_val" == "30" ]; then
	mon_loop_val=$mon_loop_val_30
	df_val="30"
elif [ "$mon_val" == "31" ]; then
	mon_loop_val=$mon_loop_val_31
	df_val="31"
else
	echo "Insert mon value[28/29/30/31]"
	exit
fi
#echo $mon_loop_val
for monloopnum in $mon_loop_val
do
	#echo "mon_loop_val:"$monloopnum
	for loopnum in $loop_val
	do
	if [ -f $file_prefix_val$date_val$monloopnum$loopnum ]; then
	 ls -al $file_prefix_val$date_val$monloopnum$loopnum
	 tar cvzf $file_prefix_val$date_val$monloopnum$loopnum$gz_val $file_prefix_val$date_val$monloopnum$loopnum
	 ls -al $file_prefix_val$date_val$monloopnum$loopnum$gz_val
	 rm -f $file_prefix_val$date_val$monloopnum$loopnum
	 ls -al $file_prefix_val$date_val$monloopnum$loopnum
	fi
	done
sleep 1
if [ "$monloopnum" == "$df_val" ]; then
	echo "========================================"
	df -h;
	echo "========================================"
fi
done
