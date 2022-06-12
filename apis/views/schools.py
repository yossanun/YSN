from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apis.models import SchoolStructure, Schools, Classes, Personnel, StudentSubjectsScore

PERSONNEL_TYPE_TEACHER = 0
PERSONNEL_TYPE_HEADROOM = 1
PERSONNEL_TYPE_STUDENT = 2


def personnel_type_text(personnel_type):
    personnel_type = int(personnel_type)
    if personnel_type == PERSONNEL_TYPE_TEACHER:
        return "Teacher"
    elif personnel_type == PERSONNEL_TYPE_HEADROOM:
        return "Head of the room"
    elif personnel_type == PERSONNEL_TYPE_STUDENT:
        return "Student"


class StudentSubjectsScoreAPIView(APIView):

    # 03/06/2022 start 14:08 PM - finish

    def get_subject(self, subject_title):

        subject_title = str(subject_title).title()

        if subject_title == 'Math':
            return 1

        elif subject_title == 'Physics':
            return 2

        elif subject_title == 'Chemistry':
            return 3

        elif subject_title == 'Algorithm':
            return 4

        elif subject_title == 'Coding':
            return 5

    def get(self, request, *args, **kwargs):

        school_name = request.GET.get("school_name", None)
        subject_title = request.GET.get("subject_title", None)

        if school_name is None:
            return Response({"message": "School's name is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if subject_title is None:
            return Response({"message": "Subject's Title is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        subject_score = StudentSubjectsScore.objects.filter(student__school_class__school__title=school_name,
                                                            subjects=self.get_subject(subject_title)).order_by("-pk")

        # print('\n'*2)
        # print(f'{subject_score[:5] = }')
        # print('\n'*2)

        score_list = [score.context_data for score in subject_score]

        return Response(score_list, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]

        # # Filter Objects Example
        # DataModel.objects.filter(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        # # Create Objects Example
        # DataModel.objects.create(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        # ---------- Get Query Params and Data from Frontend ----------------------------------------------------------
        school_name = request.GET.get("school_name", None)

        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        score = request.data.get("score", None)
        credit = request.data.get("credit", None)

        # ---------- Check Conditions When Data Error -----------------------------------------------------------------
        if student_first_name is None:
            return Response({"message": "Please specify First name."},
                            status=status.HTTP_400_BAD_REQUEST)

        if student_last_name is None:
            return Response({"message": "Please specify Last name."},
                            status=status.HTTP_400_BAD_REQUEST)

        if subjects_title is None:
            return Response({"message": "Please specify Subject's Title."},
                            status=status.HTTP_400_BAD_REQUEST)

        if score is None:
            return Response({"message": "Please specify Score."},
                            status=status.HTTP_400_BAD_REQUEST)

        if credit is None:
            return Response({"message": "Please specify Credit."},
                            status=status.HTTP_400_BAD_REQUEST)

        if type(student_first_name) != str:
            return Response({"message": "First name must be string."},
                            status=status.HTTP_400_BAD_REQUEST)

        if type(student_last_name) != str:
            return Response({"message": "Last name must be string."},
                            status=status.HTTP_400_BAD_REQUEST)

        if type(subjects_title) != str:
            return Response({"message": "Subject's title must be string."},
                            status=status.HTTP_400_BAD_REQUEST)

        if type(score) != int:
            return Response({"message": "Score must be integer."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= int(score) <= 100):
            return Response({"message": "Score must be in range 0 to 100."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not (0 < int(credit) <= 3):
            return Response({"message": "Credit must be 1, 2 or 3."},
                            status=status.HTTP_400_BAD_REQUEST)

        # ---------- Subject's Title or Student Name Not Found in Database --------------------------------------------
        if StudentSubjectsScore.objects.filter(student__first_name=student_first_name,
                                               student__last_name=student_last_name,
                                               subjects__title=subjects_title).count() == 0:

            return Response({"message": "This Subject's Name or Student's Name Not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # ---------- Update New Score in Model StudentSubjectsScore ---------------------------------------------------
        if StudentSubjectsScore.objects.filter(student__first_name=student_first_name,
                                               student__last_name=student_last_name,
                                               subjects__title=subjects_title,
                                               score__isnull=False):

            subject_score = StudentSubjectsScore.objects.get(student__first_name=student_first_name,
                                                             student__last_name=student_last_name,
                                                             subjects__title=subjects_title)

            subject_score.score = score

        # ---------- Create New Score in Model StudentSubjectsScore ---------------------------------------------------
        elif StudentSubjectsScore.objects.filter(student__first_name=student_first_name,
                                                 student__last_name=student_last_name,
                                                 subjects__title=subjects_title,
                                                 score__isnull=True):

            subject_score = StudentSubjectsScore.objects.create(student_first_name=student_first_name,
                                                                student_last_name=student_last_name,
                                                                subjects__title=subjects_title,
                                                                credit=credit,
                                                                score=score)

        subject_score.save()

        context = subject_score.context_data

        return Response(context, status=status.HTTP_201_CREATED)


class StudentSubjectsScoreDetailsAPIView(APIView):

    # 03/06/2022 start 09:55 AM - finish 14:08 PM

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        example_context_data = {
            "student":
                {
                    "id": "primary key of student in database",
                    "full_name": "student's full name",
                    "school": "student's school name"
                },

            "subject_detail": [
                {
                    "subject": "subject's title 1",
                    "credit": "subject's credit 1",
                    "score": "subject's score 1",
                    "grade": "subject's grade 1",
                },
                {
                    "subject": "subject's title 2",
                    "credit": "subject's credit 2",
                    "score": "subject's score 2",
                    "grade": "subject's grade 2",
                },
            ],
            "grade_point_average": "grade point average",
        }

        # ---------- Calculate Grade Average ---------------------------------------------------------------------------
        def cal_grade_average(subject_data):
            total_credit = 0
            total = 0
            for data in subject_data:
                total_credit += data['credit']
                total += cal_grade(data['score'])[1] * data['credit']

            grade_average = total / total_credit

            return '%.2f' % grade_average

        # ---------- Calculate Grade of Subject ------------------------------------------------------------------------
        def cal_grade(score):

            if 80 <= score <= 100:
                return "A", 4.00
            elif 75 <= score < 80:
                return "B+", 3.5
            elif 70 <= score < 75:
                return "B", 3.0
            elif 65 <= score < 70:
                return "C+", 2.5
            elif 60 <= score < 65:
                return "C", 2.0
            elif 55 <= score < 60:
                return "D+", 1.5
            elif 50 <= score < 55:
                return "D", 1
            elif score < 50:
                return "F", 0

        if student_id := kwargs.get("id", None):
            try:
                # ---------- Get Subject's score of Student ------------------------------------------------------------
                student_score_list = StudentSubjectsScore.objects.filter(student__pk=student_id)
                full_name = student_score_list.first().student.full_name
                school = student_score_list.first().student.school_class.school.title
                context_data = {}
                subject_list = []
                for student_score in student_score_list:
                    subject_list.append(
                        {
                            "subject": student_score.subjects.title,
                            "credit": student_score.credit,
                            "score": student_score.score,
                            "grade": cal_grade(student_score.score)[0]
                        }
                    )

                context_data["student"] = {"id": student_id, "full_name": full_name, "school": school}
                context_data["subject"] = subject_list
                context_data["grade_point_average"] = cal_grade_average(subject_list)

                return Response(context_data, status=status.HTTP_200_OK)

            except:
                raise NotFound(detail='Object Not Found')

        else:
            return Response({"message": "Student's ID is required."})


class PersonnelDetailsAPIView(APIView):

    # 03/06/2022 start 07:15 AM - finish 08:43 AM

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """

        data_pattern = [
            "1. school: Dorm Palace School, role: Teacher, class: 1,name: Mark Harmon",
            "2. school: Dorm Palace School, role: Teacher, class: 2,name: Jared Sanchez",
            "3. school: Dorm Palace School, role: Teacher, class: 3,name: Cheyenne Woodard",
            "4. school: Dorm Palace School, role: Teacher, class: 4,name: Roger Carter",
            "5. school: Dorm Palace School, role: Teacher, class: 5,name: Cynthia Mclaughlin",
            "6. school: Dorm Palace School, role: Head of the room, class: 1,name: Margaret Graves",
            "7. school: Dorm Palace School, role: Head of the room, class: 2,name: Darren Wyatt",
            "8. school: Dorm Palace School, role: Head of the room, class: 3,name: Carla Elliott",
            "9. school: Dorm Palace School, role: Head of the room, class: 4,name: Brittany Mullins",
            "10. school: Dorm Palace School, role: Head of the room, class: 5,name: Nathan Solis",
            "11. school: Dorm Palace School, role: Student, class: 1,name: Aaron Marquez",
            "12. school: Dorm Palace School, role: Student, class: 1,name: Benjamin Collins",
            "13. school: Dorm Palace School, role: Student, class: 1,name: Carolyn Reynolds",
            "14. school: Dorm Palace School, role: Student, class: 1,name: Christopher Austin",
            "15. school: Dorm Palace School, role: Student, class: 1,name: Deborah Mcdonald",
            "16. school: Dorm Palace School, role: Student, class: 1,name: Jessica Burgess",
            "17. school: Dorm Palace School, role: Student, class: 1,name: Jonathan Oneill",
            "18. school: Dorm Palace School, role: Student, class: 1,name: Katrina Davis",
            "19. school: Dorm Palace School, role: Student, class: 1,name: Kristen Robinson",
            "20. school: Dorm Palace School, role: Student, class: 1,name: Lindsay Haas",
            "21. school: Dorm Palace School, role: Student, class: 2,name: Abigail Beck",
            "22. school: Dorm Palace School, role: Student, class: 2,name: Andrew Williams",
            "23. school: Dorm Palace School, role: Student, class: 2,name: Ashley Berg",
            "24. school: Dorm Palace School, role: Student, class: 2,name: Elizabeth Anderson",
            "25. school: Dorm Palace School, role: Student, class: 2,name: Frank Mccormick",
            "26. school: Dorm Palace School, role: Student, class: 2,name: Jason Leon",
            "27. school: Dorm Palace School, role: Student, class: 2,name: Jessica Fowler",
            "28. school: Dorm Palace School, role: Student, class: 2,name: John Smith",
            "29. school: Dorm Palace School, role: Student, class: 2,name: Nicholas Smith",
            "30. school: Dorm Palace School, role: Student, class: 2,name: Scott Mckee",
            "31. school: Dorm Palace School, role: Student, class: 3,name: Abigail Smith",
            "32. school: Dorm Palace School, role: Student, class: 3,name: Cassandra Martinez",
            "33. school: Dorm Palace School, role: Student, class: 3,name: Elizabeth Anderson",
            "34. school: Dorm Palace School, role: Student, class: 3,name: John Scott",
            "35. school: Dorm Palace School, role: Student, class: 3,name: Kathryn Williams",
            "36. school: Dorm Palace School, role: Student, class: 3,name: Mary Miller",
            "37. school: Dorm Palace School, role: Student, class: 3,name: Ronald Mccullough",
            "38. school: Dorm Palace School, role: Student, class: 3,name: Sandra Davidson",
            "39. school: Dorm Palace School, role: Student, class: 3,name: Scott Martin",
            "40. school: Dorm Palace School, role: Student, class: 3,name: Victoria Jacobs",
            "41. school: Dorm Palace School, role: Student, class: 4,name: Carol Williams",
            "42. school: Dorm Palace School, role: Student, class: 4,name: Cassandra Huff",
            "43. school: Dorm Palace School, role: Student, class: 4,name: Deborah Harrison",
            "44. school: Dorm Palace School, role: Student, class: 4,name: Denise Young",
            "45. school: Dorm Palace School, role: Student, class: 4,name: Jennifer Pace",
            "46. school: Dorm Palace School, role: Student, class: 4,name: Joe Andrews",
            "47. school: Dorm Palace School, role: Student, class: 4,name: Michael Kelly",
            "48. school: Dorm Palace School, role: Student, class: 4,name: Monica Padilla",
            "49. school: Dorm Palace School, role: Student, class: 4,name: Tiffany Roman",
            "50. school: Dorm Palace School, role: Student, class: 4,name: Wendy Maxwell",
            "51. school: Dorm Palace School, role: Student, class: 5,name: Adam Smith",
            "52. school: Dorm Palace School, role: Student, class: 5,name: Angela Christian",
            "53. school: Dorm Palace School, role: Student, class: 5,name: Cody Edwards",
            "54. school: Dorm Palace School, role: Student, class: 5,name: Jacob Palmer",
            "55. school: Dorm Palace School, role: Student, class: 5,name: James Gonzalez",
            "56. school: Dorm Palace School, role: Student, class: 5,name: Justin Kaufman",
            "57. school: Dorm Palace School, role: Student, class: 5,name: Katrina Reid",
            "58. school: Dorm Palace School, role: Student, class: 5,name: Melissa Butler",
            "59. school: Dorm Palace School, role: Student, class: 5,name: Pamela Sutton",
            "60. school: Dorm Palace School, role: Student, class: 5,name: Sarah Murphy"
        ]

        your_result = []
        if school_title := kwargs.get("school_title", None):
            try:
                # ---------- Get Personnel Object of School name -------------------------------------------------------
                personnel = Personnel.objects.filter(school_class__school__title=school_title).order_by(
                    'personnel_type', 'school_class__class_order', 'first_name')

                for index, person in enumerate(personnel):
                    school_title = school_title.capitalize()
                    full_name = person.full_name.title()

                    data = f"{index + 1}. school: {school_title}," \
                           f" role: {personnel_type_text(person.personnel_type)}," \
                           f" class: {person.school_class.class_order}," \
                           f" name: {full_name}"

                    your_result.append(data)

                return Response(your_result, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                raise NotFound(detail='Object Not Found')

        else:
            return Response({"message": "School name is required."}, status=status.HTTP_400_BAD_REQUEST)


class SchoolHierarchyAPIView(APIView):

    # 07/06/2022 start 17:04 PM - finish 19:16 AM

    @staticmethod
    def get_personnel_classes(classes):

        data_person = []
        school_classes_person = {}

        # ---------- Get Class's Teacher -------------------------------------------------------------------------------
        personnel_teacher = Personnel.objects.filter(school_class=classes,
                                                     personnel_type=PERSONNEL_TYPE_TEACHER,
                                                     ).order_by('personnel_type', 'first_name')
        for index, teacher in enumerate(personnel_teacher):
            school_classes_person[f'{personnel_type_text(teacher.personnel_type)}: {teacher.full_name}'] = data_person

        # ---------- Get Class's Student -------------------------------------------------------------------------------
        personnel = Personnel.objects.filter(school_class=classes,
                                             personnel_type__gt=PERSONNEL_TYPE_TEACHER,
                                             ).order_by('personnel_type', 'first_name')
        for person in personnel:
            data_person.append({
                f'{personnel_type_text(person.personnel_type)}': person.full_name
            })

        return school_classes_person

    def get(self, request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "school": "Dorm Palace School",
                "class 1": {
                    "Teacher: Mark Harmon": [
                        {
                            "Head of the room": "Margaret Graves"
                        },
                        {
                            "Student": "Aaron Marquez"
                        },
                        {
                            "Student": "Benjamin Collins"
                        },
                        {
                            "Student": "Carolyn Reynolds"
                        },
                        {
                            "Student": "Christopher Austin"
                        },
                        {
                            "Student": "Deborah Mcdonald"
                        },
                        {
                            "Student": "Jessica Burgess"
                        },
                        {
                            "Student": "Jonathan Oneill"
                        },
                        {
                            "Student": "Katrina Davis"
                        },
                        {
                            "Student": "Kristen Robinson"
                        },
                        {
                            "Student": "Lindsay Haas"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Jared Sanchez": [
                        {
                            "Head of the room": "Darren Wyatt"
                        },
                        {
                            "Student": "Abigail Beck"
                        },
                        {
                            "Student": "Andrew Williams"
                        },
                        {
                            "Student": "Ashley Berg"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "Frank Mccormick"
                        },
                        {
                            "Student": "Jason Leon"
                        },
                        {
                            "Student": "Jessica Fowler"
                        },
                        {
                            "Student": "John Smith"
                        },
                        {
                            "Student": "Nicholas Smith"
                        },
                        {
                            "Student": "Scott Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Cheyenne Woodard": [
                        {
                            "Head of the room": "Carla Elliott"
                        },
                        {
                            "Student": "Abigail Smith"
                        },
                        {
                            "Student": "Cassandra Martinez"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "John Scott"
                        },
                        {
                            "Student": "Kathryn Williams"
                        },
                        {
                            "Student": "Mary Miller"
                        },
                        {
                            "Student": "Ronald Mccullough"
                        },
                        {
                            "Student": "Sandra Davidson"
                        },
                        {
                            "Student": "Scott Martin"
                        },
                        {
                            "Student": "Victoria Jacobs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Roger Carter": [
                        {
                            "Head of the room": "Brittany Mullins"
                        },
                        {
                            "Student": "Carol Williams"
                        },
                        {
                            "Student": "Cassandra Huff"
                        },
                        {
                            "Student": "Deborah Harrison"
                        },
                        {
                            "Student": "Denise Young"
                        },
                        {
                            "Student": "Jennifer Pace"
                        },
                        {
                            "Student": "Joe Andrews"
                        },
                        {
                            "Student": "Michael Kelly"
                        },
                        {
                            "Student": "Monica Padilla"
                        },
                        {
                            "Student": "Tiffany Roman"
                        },
                        {
                            "Student": "Wendy Maxwell"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Cynthia Mclaughlin": [
                        {
                            "Head of the room": "Nathan Solis"
                        },
                        {
                            "Student": "Adam Smith"
                        },
                        {
                            "Student": "Angela Christian"
                        },
                        {
                            "Student": "Cody Edwards"
                        },
                        {
                            "Student": "Jacob Palmer"
                        },
                        {
                            "Student": "James Gonzalez"
                        },
                        {
                            "Student": "Justin Kaufman"
                        },
                        {
                            "Student": "Katrina Reid"
                        },
                        {
                            "Student": "Melissa Butler"
                        },
                        {
                            "Student": "Pamela Sutton"
                        },
                        {
                            "Student": "Sarah Murphy"
                        }
                    ]
                }
            },
            {
                "school": "Prepare Udom School",
                "class 1": {
                    "Teacher: Joshua Frazier": [
                        {
                            "Head of the room": "Tina Phillips"
                        },
                        {
                            "Student": "Amanda Howell"
                        },
                        {
                            "Student": "Colin George"
                        },
                        {
                            "Student": "Donald Stephens"
                        },
                        {
                            "Student": "Jennifer Lewis"
                        },
                        {
                            "Student": "Jorge Bowman"
                        },
                        {
                            "Student": "Kevin Hooper"
                        },
                        {
                            "Student": "Kimberly Lewis"
                        },
                        {
                            "Student": "Mary Sims"
                        },
                        {
                            "Student": "Ronald Tucker"
                        },
                        {
                            "Student": "Victoria Velez"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Zachary Anderson": [
                        {
                            "Head of the room": "Joseph Zimmerman"
                        },
                        {
                            "Student": "Alicia Serrano"
                        },
                        {
                            "Student": "Andrew West"
                        },
                        {
                            "Student": "Anthony Hartman"
                        },
                        {
                            "Student": "Dominic Frey"
                        },
                        {
                            "Student": "Gina Fernandez"
                        },
                        {
                            "Student": "Jennifer Riley"
                        },
                        {
                            "Student": "John Joseph"
                        },
                        {
                            "Student": "Katherine Cantu"
                        },
                        {
                            "Student": "Keith Watts"
                        },
                        {
                            "Student": "Phillip Skinner"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Steven Hunt": [
                        {
                            "Head of the room": "Antonio Hodges"
                        },
                        {
                            "Student": "Brian Lewis"
                        },
                        {
                            "Student": "Christina Wiggins"
                        },
                        {
                            "Student": "Christine Parker"
                        },
                        {
                            "Student": "Hannah Wilson"
                        },
                        {
                            "Student": "Jasmin Odom"
                        },
                        {
                            "Student": "Jeffery Graves"
                        },
                        {
                            "Student": "Mark Roberts"
                        },
                        {
                            "Student": "Paige Pearson"
                        },
                        {
                            "Student": "Philip Fowler"
                        },
                        {
                            "Student": "Steven Riggs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Rachael Davenport": [
                        {
                            "Head of the room": "John Cunningham"
                        },
                        {
                            "Student": "Aaron Olson"
                        },
                        {
                            "Student": "Amanda Cuevas"
                        },
                        {
                            "Student": "Gary Smith"
                        },
                        {
                            "Student": "James Blair"
                        },
                        {
                            "Student": "Juan Boone"
                        },
                        {
                            "Student": "Julie Bowman"
                        },
                        {
                            "Student": "Melissa Williams"
                        },
                        {
                            "Student": "Phillip Bright"
                        },
                        {
                            "Student": "Sonia Gregory"
                        },
                        {
                            "Student": "William Martin"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Amber Clark": [
                        {
                            "Head of the room": "Mary Mason"
                        },
                        {
                            "Student": "Allen Norton"
                        },
                        {
                            "Student": "Eric English"
                        },
                        {
                            "Student": "Jesse Johnson"
                        },
                        {
                            "Student": "Kevin Martinez"
                        },
                        {
                            "Student": "Mark Hughes"
                        },
                        {
                            "Student": "Robert Sutton"
                        },
                        {
                            "Student": "Sherri Patrick"
                        },
                        {
                            "Student": "Steven Brown"
                        },
                        {
                            "Student": "Valerie Mcdaniel"
                        },
                        {
                            "Student": "William Roman"
                        }
                    ]
                }
            },
            {
                "school": "Rose Garden School",
                "class 1": {
                    "Teacher: Danny Clements": [
                        {
                            "Head of the room": "Troy Rodriguez"
                        },
                        {
                            "Student": "Annette Ware"
                        },
                        {
                            "Student": "Daniel Collins"
                        },
                        {
                            "Student": "Jacqueline Russell"
                        },
                        {
                            "Student": "Justin Kennedy"
                        },
                        {
                            "Student": "Lance Martinez"
                        },
                        {
                            "Student": "Maria Bennett"
                        },
                        {
                            "Student": "Mary Crawford"
                        },
                        {
                            "Student": "Rodney White"
                        },
                        {
                            "Student": "Timothy Kline"
                        },
                        {
                            "Student": "Tracey Nichols"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Ray Khan": [
                        {
                            "Head of the room": "Stephen Johnson"
                        },
                        {
                            "Student": "Ashley Jones"
                        },
                        {
                            "Student": "Breanna Baker"
                        },
                        {
                            "Student": "Brian Gardner"
                        },
                        {
                            "Student": "Elizabeth Shaw"
                        },
                        {
                            "Student": "Jason Walker"
                        },
                        {
                            "Student": "Katherine Campbell"
                        },
                        {
                            "Student": "Larry Tate"
                        },
                        {
                            "Student": "Lawrence Marshall"
                        },
                        {
                            "Student": "Malik Dean"
                        },
                        {
                            "Student": "Taylor Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Jennifer Diaz": [
                        {
                            "Head of the room": "Vicki Wallace"
                        },
                        {
                            "Student": "Brenda Montgomery"
                        },
                        {
                            "Student": "Daniel Wilson"
                        },
                        {
                            "Student": "David Dixon"
                        },
                        {
                            "Student": "John Robinson"
                        },
                        {
                            "Student": "Kimberly Smith"
                        },
                        {
                            "Student": "Michael Miller"
                        },
                        {
                            "Student": "Miranda Trujillo"
                        },
                        {
                            "Student": "Sara Bruce"
                        },
                        {
                            "Student": "Scott Williams"
                        },
                        {
                            "Student": "Taylor Levy"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Kendra Pierce": [
                        {
                            "Head of the room": "Christopher Stone"
                        },
                        {
                            "Student": "Brenda Tanner"
                        },
                        {
                            "Student": "Christopher Garcia"
                        },
                        {
                            "Student": "Curtis Flynn"
                        },
                        {
                            "Student": "Jason Horton"
                        },
                        {
                            "Student": "Julie Mullins"
                        },
                        {
                            "Student": "Kathleen Mckenzie"
                        },
                        {
                            "Student": "Larry Briggs"
                        },
                        {
                            "Student": "Michael Meyer"
                        },
                        {
                            "Student": "Tammy Smith"
                        },
                        {
                            "Student": "Thomas Martinez"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Elizabeth Hebert": [
                        {
                            "Head of the room": "Caitlin Lee"
                        },
                        {
                            "Student": "Alexander James"
                        },
                        {
                            "Student": "Amanda Weber"
                        },
                        {
                            "Student": "Christopher Clark"
                        },
                        {
                            "Student": "Devin Morgan"
                        },
                        {
                            "Student": "Gary Clark"
                        },
                        {
                            "Student": "Jenna Sanchez"
                        },
                        {
                            "Student": "Jeremy Meyers"
                        },
                        {
                            "Student": "John Dunn"
                        },
                        {
                            "Student": "Loretta Thomas"
                        },
                        {
                            "Student": "Matthew Vaughan"
                        }
                    ]
                }
            }
        ]

        try:
            # ---------- Get School's name -----------------------------------------------------------------------------
            school_list = Schools.objects.all().order_by('title')
            your_result = []
            for index, school in enumerate(school_list):
                your_result.append({
                    "school": school.title
                })
                # ---------- Get School's Class ------------------------------------------------------------------------
                classes_list = Classes.objects.filter(school=school).order_by('class_order')
                for classes in classes_list:
                    your_result[index][f'class {classes.class_order}'] = self.get_personnel_classes(classes)

            return Response(your_result, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "Object not found."}, status=status.HTTP_400_BAD_REQUEST)


class SchoolStructureAPIView(APIView):

    # 03/06/2022 start 14:08 AM - finish 16:44 AM

    def get_child_location(self, parent_school_structure):
        school_structures_child = []
        # ---------- Get Child of School Structure Object -------------------------------------------------------
        school_structures = SchoolStructure.objects.filter(parent=parent_school_structure).order_by('pk')

        for index, school_structure in enumerate(school_structures):
            school_structures_child.append({
                "title": school_structure.title
            })

            # ---------- Get Child of Parent School Structure Object ---------------------------------------------------
            sub_school_structures = SchoolStructure.objects.filter(parent=school_structure).order_by('pk')
            if len(sub_school_structures) > 0:
                school_structures_child[index]['sub'] = self.get_child_location(school_structure)

        return school_structures_child

    def get(self, request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "title": "มัธยมต้น",
                "sub": [
                    {
                        "title": "ม.1",
                        "sub": [
                            {
                                "title": "ห้อง 1/1"
                            },
                            {
                                "title": "ห้อง 1/2"
                            },
                            {
                                "title": "ห้อง 1/3"
                            },
                            {
                                "title": "ห้อง 1/4"
                            },
                            {
                                "title": "ห้อง 1/5"
                            },
                            {
                                "title": "ห้อง 1/6"
                            },
                            {
                                "title": "ห้อง 1/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.2",
                        "sub": [
                            {
                                "title": "ห้อง 2/1"
                            },
                            {
                                "title": "ห้อง 2/2"
                            },
                            {
                                "title": "ห้อง 2/3"
                            },
                            {
                                "title": "ห้อง 2/4"
                            },
                            {
                                "title": "ห้อง 2/5"
                            },
                            {
                                "title": "ห้อง 2/6"
                            },
                            {
                                "title": "ห้อง 2/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.3",
                        "sub": [
                            {
                                "title": "ห้อง 3/1"
                            },
                            {
                                "title": "ห้อง 3/2"
                            },
                            {
                                "title": "ห้อง 3/3"
                            },
                            {
                                "title": "ห้อง 3/4"
                            },
                            {
                                "title": "ห้อง 3/5"
                            },
                            {
                                "title": "ห้อง 3/6"
                            },
                            {
                                "title": "ห้อง 3/7"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "มัธยมปลาย",
                "sub": [
                    {
                        "title": "ม.4",
                        "sub": [
                            {
                                "title": "ห้อง 4/1"
                            },
                            {
                                "title": "ห้อง 4/2"
                            },
                            {
                                "title": "ห้อง 4/3"
                            },
                            {
                                "title": "ห้อง 4/4"
                            },
                            {
                                "title": "ห้อง 4/5"
                            },
                            {
                                "title": "ห้อง 4/6"
                            },
                            {
                                "title": "ห้อง 4/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.5",
                        "sub": [
                            {
                                "title": "ห้อง 5/1"
                            },
                            {
                                "title": "ห้อง 5/2"
                            },
                            {
                                "title": "ห้อง 5/3"
                            },
                            {
                                "title": "ห้อง 5/4"
                            },
                            {
                                "title": "ห้อง 5/5"
                            },
                            {
                                "title": "ห้อง 5/6"
                            },
                            {
                                "title": "ห้อง 5/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.6",
                        "sub": [
                            {
                                "title": "ห้อง 6/1"
                            },
                            {
                                "title": "ห้อง 6/2"
                            },
                            {
                                "title": "ห้อง 6/3"
                            },
                            {
                                "title": "ห้อง 6/4"
                            },
                            {
                                "title": "ห้อง 6/5"
                            },
                            {
                                "title": "ห้อง 6/6"
                            },
                            {
                                "title": "ห้อง 6/7"
                            }
                        ]
                    }
                ]
            }
        ]

        try:
            # ---------- Get only Parent of School Structure Object ----------------------------------------------------
            school_structures = SchoolStructure.objects.filter(parent=None).order_by('pk')
            your_result = []

            for index, school_structure in enumerate(school_structures):
                your_result.append({
                    "title": school_structure.title,
                })

                # ---------- Get Child of School Structure Object ------------------------------------------------------
                sub_school_structure = SchoolStructure.objects.filter(parent=school_structure).order_by('pk')
                if len(sub_school_structure) > 0:
                    your_result[index]['sub'] = self.get_child_location(school_structure)

                else:
                    your_result[index]['sub'] = []

            return Response(your_result, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"message": "Object not found."}, status=status.HTTP_400_BAD_REQUEST)
