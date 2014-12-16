
# -----------------------------------------------------------------------
# AWS Crendentials
#
# Be aware of the security threaten if these keys would be leaked to bad people
# -----------------------------------------------------------------------

aws_credentials = {'dev_account':{'ACCESS_KEY':'', 'SECRET_KEY':''},
                   'stg_account':{'ACCESS_KEY':'', 'SECRET_KEY':''},
                   'prd_account':{'ACCESS_KEY':'', 'SECRET_KEY':''}}

# MUST BE SAME AS THE ACCOUNT NAME AND THEIR ORDERS ABOVE!
account_list = ['dev_account', 'stg_account', 'prd_account']
