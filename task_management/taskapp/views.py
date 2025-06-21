from django.shortcuts import render
from .models import TaskDetails
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

# Create your views here.

class OverallTasksAPi(APIView):
    def get(self,request):
        try:
            data=request.query_params
            task_status=data.get('status',None)
            due_date=data.get('due_date',None)
            start_index=data.get('start_index',0)
            #default 10 counts,per-page data
            end_index= data.get('count',10)
            details=[]
     
            task_object = TaskDetails.objects.filter(is_active=True)
            task_count = task_object.count()
            next_index = 10
            if task_count>10:
                next_index = task_count+1
            if task_status is not None:
                task_object = task_object.filter(status=task_status)
            elif due_date is not None:
                dateformat=datetime.datetime.strptime(due_date,"%Y-%m-%d")
                task_object = task_object.filter(due_date=dateformat)
            #if you want pagenation use count and startwith, and result will be per-page 10 result
            task_object = task_object[int(start_index):int(end_index)]

            for obj  in task_object:
                details.append({
                    "title":obj.title,
                    "description":obj.description,
                    "status":obj.status,
                    "due_date":obj.due_date,
                    "created_at":round(obj.created_at.timestamp()),
                    "updated_at":round(obj.updated_at.timestamp() if obj.updated_at else 0),
                })
            return Response({"status":"success","message":"Data fetched successfully","data":details,"task_count":task_count,"next_index":next_index},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"error","message":"Something went wrong "+str(e),"data":None},status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        try:
            data=request.data
            title=data.get('title')
            description=data.get('description','')
            due_date=data.get('due_date')
            dateformat=datetime.datetime.strptime(due_date,"%Y-%m-%d")
            task_obj = TaskDetails(title=title,description=description,due_date=dateformat)
            task_obj.save()
            return Response({"status":"success","message":"Data created successfully","data":task_obj.id},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status":"error","message":"Something went wrong "+str(e),"data":None},status=status.HTTP_400_BAD_REQUEST)


class TasksAPi(APIView):
    def get(self,request,id):
        try:
            data=request.query_params
            task_status=data.get('status',None)
            details=[]
            if id is not None:
                try:
                    obj = TaskDetails.objects.get(id=id,is_active=True)
                except:
                    return Response({"status":"error","message":"Task not found or deleted by user"},status=status.HTTP_400_BAD_REQUEST)

                details={
                    "title":obj.title,
                    "description":obj.description,
                    "status":obj.status,
                    "due_date":obj.due_date,
                    "created_at":round(obj.created_at.timestamp()),
                    "updated_at":round(obj.updated_at.timestamp() if obj.updated_at else 0),
                }
            return Response({"status":"success","message":"Data fetched successfully","data":details},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"error","message":"Something went wrong "+str(e),"data":None},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):
        try:
            data=request.data
            title=data.get('title')
            description=data.get('description','')
            user_status=data.get('status','pending')
            due_date=data.get('due_date',None)
            if due_date is not None:
                dateformat=datetime.datetime.strptime(due_date,"%Y-%m-%d")
            try:
                task_obj = TaskDetails.objects.get(id=id,is_active=True)
            except:
                return Response({"status":"error","message":"Task not found or deleted by user"},status=status.HTTP_400_BAD_REQUEST)
            
            task_obj.title=title
            task_obj.description=description
            task_obj.status=user_status
            if due_date is not None:
                task_obj.due_date=dateformat
            task_obj.save()
            return Response({"status":"success","message":"Data updated successfully"},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status":"error","message":"Something went wrong "+str(e),"data":None},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            data=request.data
            try:
                task_obj = TaskDetails.objects.get(id=id,is_active=True)
            except:
                return Response({"status":"error","message":"Task is not found or user already deleted the task"},status=status.HTTP_400_BAD_REQUEST)
            
            task_obj.is_active=False
            task_obj.save()
            return Response({"status":"success","message":"Data deleted successfully"},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status":"error","message":"Something went wrong "+str(e),"data":None},status=status.HTTP_400_BAD_REQUEST)

