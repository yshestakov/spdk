#
# Regular cron jobs for the spdk package
#
0 4	* * *	root	[ -x /usr/bin/spdk_maintenance ] && /usr/bin/spdk_maintenance
