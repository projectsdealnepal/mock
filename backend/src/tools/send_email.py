# def email_to_branch(request, atm, upload_method='bulk'):
    
#     from string import Template

#     import datetime
#     import requests
#     import json
#     from django.shortcuts import get_object_or_404
#     # from custom import zibra_email

#     f_isSendextraEmail = request.POST.get('extraEmails')

#     f_error = request.POST.get('error_details')
#     #available_keywords  = "atm, days, hours, minutes, date, error, responsible, additional_status, branch_name"
#     atm_obj = models.AtmTerminal.objects.get(id=atm.id)
#     branch_obj = models.BranchDetails.objects.get(id=atm_obj.branch.id)
#     error_inst = get_object_or_404(models.AtmErrorList, id=int(f_error))
    
#     atm_location = atm_obj.location
#     oi_email = branch_obj.operation_officer_email_address
#     bm_email = branch_obj.branch_manager_email_address

#     oi_email = 'ashok.dhakal@sbl.com.np'
#     bm_email = 'raj.ranjitkar@sbl.com.np'

#     temp_inst = models.EmailTemplate.objects.filter(error = error_inst)

#     to = [oi_email]
#     cc = [bm_email]
#     if upload_method == 'manual':
#         if f_isSendextraEmail:
#             add_email = f_isSendextraEmail.split(',')
#             cc.extend(add_email)
 

#     downtime = models.Downtime.objects.filter(atm=atm).last()
#     # if downtime.is_countable == 'yes':
#     #     temp_inst = models.EmailTemplate.objects.filter(template_type = 'email_for_down_atm')

#     # else:
#     #     temp_inst = models.EmailTemplate.objects.filter(template_type = 'email_for_working_atm')

#     template =temp_inst.values_list('template_content').last()[0]
    
#     subject = temp_inst.values_list('template_subject').last()[0]


#     t = Template(template)
#     sub = Template(subject)

    
#     email_content = t.safe_substitute(
#         atm=downtime.atm.name,
#         branch_name=downtime.atm.branch.branch_name,
#         days=downtime.days,
#         hours=downtime.hours,
#         minutes=downtime.minutes,
#         date=downtime.date,
#         error=downtime.error.error_details,
#         responsible=downtime.responsible.party_name,
#         additional_status=downtime.additional_status.status,
#         location = atm_location,
#     )

#     subject_content = sub.safe_substitute(
#         atm=downtime.atm.name,
#         branch_name=downtime.atm.branch.branch_name,
#         days=downtime.days,
#         hours=downtime.hours,
#         minutes=downtime.minutes,
#         date=downtime.date,
#         error=downtime.error.error_details,
#         responsible=downtime.responsible.party_name,
#         additional_status=downtime.additional_status.status,
#         location = atm_location,
#     )

#     try:
#         zibra_email(to, subject_content, body='', cc=cc, htmlbody=email_content)
#         sent_status = 'success'
#     except Exception as e:
#         sent_status = 'failed'

#     models.EmailHistory.objects.create( 
#         sent_status = sent_status,
#         email_content = email_content,
#         email_subject = subject,
#         server_response = 'sent',
#         email_to = to,
#         email_cc = cc,
#         branch_name = branch_obj,
#         sent_by = request.user
#         )