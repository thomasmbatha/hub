Leave
# leave
## Templates
<!-- =============================================
==================================================          ---------------------TEMPLATE---------------------
==================================================
============================================== -->


<!-- =============================================
    LEAVE FORM 
============================================== -->
### [x] Leave form

* Type of Leave (select)
    - Annual
    - Sick
    - Maternity
    - Paternity
    - Emergency
    - Study
    - Unpaid

* Date (date)
    - Start Date

* Date (date)
    - End Date

* Number of Days (number)
    - eg 5 days

* Shift (select)
    - Manager

* Reason (text field)
    - Note

* Attachment (attachment field)
    - [-] Depending on the type of leave

<!-- =============================================
    LEAVE OVERVIEW
============================================== -->

### [x] Leave Overview
- Days left
- Days Used
- Pending approval

- Last approved status (10 Apr 2026)
- Next Leave (20 Apr 2026)
- Remaining time until forced leave: (7 months, 26 days)

<!-- =============================================
    LEAVE RECORDS 
============================================== -->
### [x] Leave Table
- Date of the leave taken
- Type of leave
- Status
- PDF file to show previous leave

<!-- =============================================
    SHIFT LEAVE TABLE
============================================== -->
### [x] Leave Table
- Employee Name
    * Yosepha
- Job Tittle
    * Ramp Controller
- Leave Type
    * Annual
- From & To
    * 01 Apr 2026 to 05 Apr 2026


<!-- =============================================
==================================================          ------------------Functionalities-----------------
==================================================
============================================== -->


## Apply for Leave
* [] If max people are on leave the system should not allow more than 2 people on leave, The system should automatically kick you out and ask you if you want to request a special leave.

* [] The special request leave should ask for permission from the Senior via whatsApp to grant access or deny it.

* [] On a staff member's birthday they get the first prefference 

* [] If an employee requests a Sick, Maternity, Paternity, Emergency or Study leave, they should upload the sick note.
* [] The leave must be blocked for special days and December.


## Leave Overview
* [] The system must calculate how many days left
* [] The system must calculate how many days used
* [] The system must calculate how many leave applications are pending
* [] The last date of the approved leave
* [] Next Leave date
* [] Force leave update
    - If the force Leave is one month left, then is should be writtern in red other wise it must be green and yellow for 3 months.

## Leave Records
* [] View All - This should open a modal and show all the previous leave records
* [] The Pending must be automatically be substituted by the approved, declined, cancelled or rejected.
* [] PDF button must have a modal to view the report that can be downloaded into a PDF file and a close button.
* [] The system must show the date a leave form was submitted, or any other action. (approved, rejected, cancelled...etc)
* [] The system must show the which type of leave was taken

## Leave Table
* []  A day fter they return the leave must be removed from the table
* []  The system must show who took leave. (name of the employee)
* []  Their job title
* []  Type of leave they took
* []  From when till when
* []  Additional button must be added to show the full table
