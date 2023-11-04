jkm = "Joseph Kwesi Mensah cv.docx"
name = jkm.split('.')
# print(name[0])
jkk = "{}".format(jkm.split(".")[0])
print(jkk)

# files = request.FILES.getlist('file')
#         if file_form.is_valid():
#             for f in files:
#                 unique_id = get_random_string(length=2)
#                 case_title ="{}".format(f.name.split(".")[0])
#                 new_files = CaseFile.objects.create(
#                     case=case, title=case_title, file=f)
#                 print(f.name)
#                 print(new_files)
#                 add_log(request.user.pk,new_files,"added case files")

# for f in files:
            #     file_name = files
            #     print(file_name)
            #     unique_id = get_random_string(length=2)
            #     case_title ="{}".format(f.name.split(".")[0])
            #     new_files = CaseFile.objects.create(
            #         case=case, title=case_title, file=f)
            #     print(f.name)
            #     print(new_files)
            #     add_log(request.user.pk,new_files,"added case files")