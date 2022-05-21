import json
import os,sys


class jobs():
    def __init__(self, jenkins_data_file):
        self.jenkins_data_file = jenkins_data_file

    #niepotrzebna:
    def jobs_amount_string(self,job_lista_str):
        return job_lista_str.count('jobs')

    def print_jobs_amount(self):
         if os.path.isfile(self.jenkins_data_file):
            f = open(self.jenkins_data_file,"r",encoding='UTF8')
            job_lista = f.read()
            job_list_dict = json.loads(job_lista)
            i = 0
            for job in job_list_dict["jobs"]:
                i += 1
            f.close()
            return i
         else:
             print("File doesn't exists")
             sys.exit

    def get_jobs(self):
        job_lista = self.open_json_file()
        if job_lista != None:
            job_list_dict = json.loads(job_lista)["jobs"]
            return job_list_dict
        else:
            print("File doesn't exists")
            sys.exit

    def open_json_file(self):
        if os.path.isfile(self.jenkins_data_file):
            f = open(self.jenkins_data_file,"r",encoding='UTF8')
            job_lista = f.read()
            f.close()
            return job_lista
        else:
            print("File doesn't exists")
            sys.exit


    def print_jobs(self, job_lista):
         if job_lista != None:
            job_list_dict = json.loads(job_lista)
            print("Job id: |Job name:   |Build number: ")
            for job in job_list_dict["jobs"]:
               print("Job ",job.get("job_nr"),":",job.get("job_name"))
               print("  Build: ",job.get("builds"))
               if job.get("last_build_date") != {}:
                   print("  Build date: ",job.get("last_build_date"))
                   print(" ",job.get("who_started_build"))
                   print("  Build state:",job.get("success_build"))
         else:
            print("File probably doesn't exists")
            sys.exit

    def sortJobsByDateDesc(self,job_lista, iLow, iHigh):
        if iLow >= iHigh or iLow <0 or iHigh <0:
            return
        compare_list = job_lista[iLow]
        lowersNumsEndIndex = iLow + 1
        for i in range(iLow+1,iHigh+1):
            if job_lista[i]['last_build_date'] == {}:
                rob_list = job_lista[iHigh]
                job_lista[iHigh] = job_lista[i]
                job_lista[i] = rob_list
            if job_lista[i]['last_build_date'] != {} and compare_list['last_build_date'] != {}:
                if job_lista[i]['last_build_date'] >= compare_list['last_build_date']:
                    rob_list = job_lista[i]
                    job_lista[i] = job_lista[lowersNumsEndIndex]
                    job_lista[lowersNumsEndIndex] = rob_list
                    lowersNumsEndIndex += 1
        rob_list = job_lista[iLow]
        job_lista[iLow] = job_lista[lowersNumsEndIndex-1]
        job_lista[lowersNumsEndIndex-1] = rob_list
        self.sortJobsByDateDesc(job_lista, iLow, lowersNumsEndIndex-2)
        self.sortJobsByDateDesc(job_lista, lowersNumsEndIndex, iHigh)
        return job_lista

    def sortJobsByBuildNrDesc(self,job_lista, iLow, iHigh):
        #jobs_list = self.AllJobs()
        #stop:
        if iLow >= iHigh or iLow <0 or iHigh <0:
            return
        compare_list = job_lista[iLow]
        lowersNumsEndIndex = iLow + 1
        for i in range(iLow+1,iHigh+1):
            if job_lista[i]['builds'] >= compare_list['builds']:
                rob_list = job_lista[i]
                job_lista[i] = job_lista[lowersNumsEndIndex]
                job_lista[lowersNumsEndIndex] = rob_list
                lowersNumsEndIndex += 1
        rob_list = job_lista[iLow]
        job_lista[iLow] = job_lista[lowersNumsEndIndex-1]
        job_lista[lowersNumsEndIndex-1] = rob_list
        self.sortJobsByBuildNrDesc(job_lista, iLow, lowersNumsEndIndex-2)
        self.sortJobsByBuildNrDesc(job_lista, lowersNumsEndIndex, iHigh)
        return job_lista

    def saveToJsonFile(self, job_lista, filename):
        f = open(filename,"w")
        f.write("{ \n" )
        f.write("\n")
        f.write(" \"jobs\" : [ \n")
        f.write("\n")
        l = len(job_lista)
        for job in job_lista:
            l -= 1
            rob = str(job)
            rob = rob.replace('\'', '\"')
            if l == 0:
                f.write("    ")
                f.write(rob)
                f.write("\n")
            else:
                f.write("    ")
                f.write(rob)
                f.write(",\n")
            f.write("\n")

        f.write(" ] \n")
        f.write("\n")
        f.write("}")
        print("Data saved in file: ", filename)
        f.close

    def coutSuccessJobs(self,jobs):
        suc = 0
        fail = 0
        for job in jobs:
            if job['success_build'] =='SUCCESS':
                suc +=1
            elif job['success_build'] == 'FAILURE':
                fail +=1
        return suc, fail

    def changeStateToUnstableJSonFile(self,job_lista):
        for job in job_lista:
            if job['success_build'] =='SUCCESS':
                job['success_build'] = ' UNSTABLE'
            elif job['success_build'] =='FAILURE':
                job['success_build'] = ' UNSTABLE'
        return job_lista

jenkins_data_file = jobs("./json_file/jenkins_data.json")
job_lista = jenkins_data_file.open_json_file()
jobs_amount = jenkins_data_file.print_jobs_amount()
print("Jobs amount: ",jobs_amount)
print('Choose what do you want to do:')
print('1 - show all the jobs with the last build done from JSON file')
print('2 - sort descending by date and show')
print('3 - sort descending by build number and show')
print('4 - show all jobs (you can sort them earlier by date or build number) in JSON format on screen')
print('5 - show all jobs (you can sort them earlier by date or build number) in JSON format in a written json file')
print('6 - show the count of failed/ passed jobs')
print('7 - change in JSon file all \"failed\"/ \"success\" to \"unstable\" in new output JSON format file')
print('8 - close the program')
x = input('your choice: ')
i = 1
while not (x in ['1','2','3','4','5','6','7','8']):
    x = input('Make the correct choice again:')
    i += 1
    if i >= 5:
        exit
if x == '1' :
    jenkins_data_file.print_jobs(job_lista)
elif x == '2':
    job_list_dict = json.loads(job_lista).get("jobs")
    jobs_sorted = jenkins_data_file.sortJobsByDateDesc(job_list_dict, 0, jobs_amount-1)
    jobs = {"jobs":jobs_sorted}
    jenkins_data_file.print_jobs(json.dumps(jobs))
elif x == '3':
    job_list_dict = json.loads(job_lista).get("jobs")
    jobs_sorted = jenkins_data_file.sortJobsByBuildNrDesc(job_list_dict, 0, jobs_amount-1)
    jobs = {"jobs":jobs_sorted}
    jenkins_data_file.print_jobs(json.dumps(jobs))
elif x == '4':
    job_list_dict = json.loads(job_lista).get("jobs")
    odp = input('Do you want to sort it by date? (y/n): ')
    jobs_sorted = None
    if odp == "Y" or odp == "y":
        jobs_sorted = jenkins_data_file.sortJobsByDateDesc(job_list_dict, 0, jobs_amount-1)
    else:
        odp = input('Do you want to sort it by build number? (y/n): ')
        if odp == "Y" or odp == "y":
            jobs_sorted = jenkins_data_file.sortJobsByBuildNrDesc(job_list_dict, 0, jobs_amount-1)
    if jobs_sorted != None:
        jobs = {"jobs":jobs_sorted}
    else:
        jobs = job_list_dict
    print(jobs)
elif x == '5':
    job_list_dict = json.loads(job_lista).get("jobs")
    odp = input('Do you want to sort it by date? (y/n): ')
    jobs = job_list_dict
    if odp == "Y" or odp == "y":
        jobs_sorted = jenkins_data_file.sortJobsByDateDesc(job_list_dict, 0, jobs_amount-1)
        jobs = jobs_sorted
    else:
        odp = input('Do you want to sort it by build number? (y/n): ')
        if odp == "Y" or odp == "y":
            jobs_sorted = jenkins_data_file.sortJobsByBuildNrDesc(job_list_dict, 0, jobs_amount-1)
            jobs = jobs_sorted
    filename = "./json_file/jenkins_data_output.json"
    jenkins_data_file.saveToJsonFile(jobs, filename)
elif x == '6':
    job_list_dict = json.loads(job_lista).get("jobs")
    jobs_success = jenkins_data_file.coutSuccessJobs(job_list_dict)[0]
    jobs_failed = jenkins_data_file.coutSuccessJobs(job_list_dict)[1]
    print("Success jobs: ",jobs_success)
    print("Failed jobs: ", jobs_failed)
elif x == '7':
    job_list_dict = json.loads(job_lista).get("jobs")
    jobs = jenkins_data_file.changeStateToUnstableJSonFile(job_list_dict)
    filename = "./json_file/jenkins_data_output.json"
    jenkins_data_file.saveToJsonFile(jobs, filename)
elif x == '8':
    print('Program closed')
    exit
else:
    exit
