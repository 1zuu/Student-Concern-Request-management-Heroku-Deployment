# Student-Concern-Request-management
# Student-Concern-Request-management-Heroku-Deployment

DB URL : mongodb+srv://admin:<password>@cluster0.lx3sd.mongodb.net/test

REQUEST 1 : {"Gender"  : "Female", "Age Group" : "21-25", "Year" : "3"}
           
REQUEST 2 : {"concern" : "Can I join to mulitiple sports teams?"}
            {"concern" : "There were more flies in the canteen."}

heroku logs --tail --app student-concern-request-manage

##########################  GET APIs  ########################
https://student-concern-request-manage.herokuapp.com/concern
https://student-concern-request-manage.herokuapp.com/Complaint
https://student-concern-request-manage.herokuapp.com/Request




http://192.168.1.4:5000/concern


https://cloud.mongodb.com/v2/6128eb4999d5a9014c4595f8#clusters