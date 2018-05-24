import gitlab
from sys import argv

script, zone = argv

gl = gitlab.Gitlab('<HTTPS URL OF GITLAB SERVER>','<APIKEY>')
gl.auth()
url = 'https://<GITLABSERVER>/dns/private/%s' % zone
groups = gl.groups.get(587)
project = gl.projects.create({'name':'%s' % zone,'namespace_id':587,'visibility_level':20,'request_access_enabled':True,'only_allow_merge_if_build_succeeds':True,'approvals_before_merge':1,'only_allow_merge_if_all_discussions_are_resolved':True,'web_url':'https://<GITLAB SERVER>/dns/public/%s' % zone,'path_with_namespace':'something/dns/public/%s' % zone,'name_with_namespace':'something / dns / public / %s' % zone,'ssh_url_to_repo':'git@<Gitlab SERVER>:something/dns/private/%s.git' % zone,'path':'%s' % zone,})
var1 = project.variables.create({'key': 'AWS_ACCESS_KEY_ID', 'value': 'blank'})
var2 = project.variables.create({'key': 'AWS_SECRET_ACCESS_KEY', 'value': 'blank'})
var3= project.variables.create({'key': 'DEV_AWS_ACCESS_KEY_ID', 'value': 'blank'})
var4 = project.variables.create({'key': 'DEV_AWS_SECRET_ACCESS_KEY', 'value': 'blank'})
