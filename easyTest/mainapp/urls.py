from django.urls import path
import mainapp.views as mainapp
from pathlib import PurePath
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('redirect/<slug:slug>/', mainapp.UsersRedirectView.as_view(), name='redirect'),

    path('test/create/', mainapp.TestCreate.as_view(), name='test_create'),
    path('test/edit/<int:pk>', mainapp.TestEdit.as_view(), name='test_edit'),
    path('test/<int:pk>', mainapp.QuestionList.as_view(), name='test'),
    path('test/<int:pk>/delete/', mainapp.TestDelete.as_view(), name='test_delete'),
    path('tests/', mainapp.TestList.as_view(), name='tests'),
    path('tests/staff/', mainapp.StaffTestList.as_view(), name='tests_staff'),
    path('test/<int:pk>/export/', mainapp.TestDetail.as_view(), name='test_export'),

    path('question_create/', mainapp.QuestionCreate.as_view(), name='question_create'),
    path('question_edit/<int:pk>/', mainapp.QuestionUpdate.as_view(), name='question_edit'),
    path('question/<int:pk>/delete/', mainapp.QuestionDelete.as_view(), name='question_delete'),
    path('question/staff/', mainapp.StaffQuestionList.as_view(), name='questions_staff'),

    path('results/<int:pk>/', mainapp.ResultList.as_view(), name='results'),
    path('result/<int:pk>/test_<int:test>', mainapp.ResultDetail.as_view(), name='result'),
    path('result/create/<int:test>/', mainapp.ResultCreate.as_view(), name='result_create'),
    path('result/edit/<int:test>/', mainapp.ResultUpdate.as_view(), name='result_update'),

    path('category/create/', mainapp.TestCategoryCreate.as_view(), name='category_create'),
    path('category/edit/<int:pk>', mainapp.TestCategoryEditView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', mainapp.TestCategoryDelete.as_view(), name='testcategory_delete'),
    path('category/list/', mainapp.TestCategoryList.as_view(), name='testcategory_list'),

    path('test_time_is_over/<int:test>', mainapp.TestTimeIsOver.as_view(), name='test_time_is_over'),

    path('groups/', mainapp.GroupList.as_view(), name='groups'),
    path('group/create/', mainapp.GroupCreate.as_view(), name='group_create'),
    path('group/edit/<int:pk>/', mainapp.GroupUpdate.as_view(), name='group_update'),
    path('group/<int:pk>/delete/', mainapp.GroupDelete.as_view(), name='group_delete'),
    path('group/<int:pk>/', mainapp.GroupDetail.as_view(), name='group'),

    path('students/', mainapp.StudentList.as_view(), name='students'),
    path('student/create/', mainapp.StudentCreate.as_view(), name='student_create'),
    path('student/<int:pk>', mainapp.StudentUpdate.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', mainapp.StudentDelete.as_view(), name='student_delete'),

    ]