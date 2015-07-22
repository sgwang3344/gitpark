# encoding=UTF-8
from django.shortcuts import render, render_to_response
from blog.models import *
from django.http import HttpResponse
from django import forms
import jieba  # 需要安装结巴分词模块！！！！！
import re
import pytz


jieba.load_userdict("/home/wangshigang/workspace/zhongjie/src/blog/userdict.txt") 
class UserForm(forms.Form):
    search = forms.CharField()

def show(req):
    
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():

            emp = form.cleaned_data
            str = emp['search']
            print emp['search']
      
            test_sent = str
            time_sent = str
            words = jieba.cut(test_sent)
            
        manager_information = None
        house_information = None
            
        try :
            for w in words:
                if Group.objects.filter(name__icontains=w).count() > 0:
                    groupemp = Group.objects.filter(name__icontains=w)
                    print groupemp
                    searched_group = groupemp[0]
                    
                    house_boo = True
                    manager_boo = True
                    break

      
            # find租赁

            if  time_sent.find(u'租赁') != -1:
                house_boo = True
                manager_boo = False
                
                house_information = House.objects.filter(group__name__icontains=searched_group)
                
                month_pattern = re.compile(r'\d+' + u'月')
                year_pattern = re.compile(r'[0-9]+' + u'年')
                
                month_match = month_pattern.search(time_sent)
                
                year_match = year_pattern.search(time_sent)

                # print 'time ?',time_sent.index('\d')
                if month_match:
                    time_result = month_match.group()
                    time_result = time_result[0:len(time_result) - 1]
                    house_information = house_information.filter(date__month=time_result)
                if year_match:
                    time_result = year_match.group()
                    time_result = time_result[0:len(time_result) - 1]
                    house_information = house_information.filter(date__year=time_result)

                # price filter
               
                if time_sent.find(u'价格') != -1:
                    if time_sent.find(u'大于') != -1:
                        gte_partten = re.compile(u'大于' + r'\d+')
                        gte_match = gte_partten.search(time_sent)
                        print gte_match
                        # print 'come in'
                        if gte_match:
                            price_result = gte_match.group()
                            gte_partten = re.compile(r'\d+')
                            price_result = gte_partten.search(price_result).group()
                            house_information = house_information.filter(price__gte=price_result)
                            print house_information
                            
                    elif time_sent.find(u'小于') != -1:
                        lte_partten = re.compile(u'小于' + r'\d+')
                        lte_match = lte_partten.search(time_sent)
                        print lte_match
                        if lte_match:
                            price_result = lte_match.group()
                            lte_partten = re.compile(r'\d+')
                            price_result = lte_partten.search(price_result).group()
                            house_information = house_information.filter(price__lte=price_result)


            # find经纪人
            if  time_sent.find(u'经纪人') != -1:
                manager_boo = True
                house_boo = False
                manager_information = Manager.objects.filter(group__name=searched_group)
                
            nothing_boo = False
            
            return render_to_response('output.html',
                                      {'searched_group':searched_group,
                                       'house_boo':house_boo,
                                       'house_information':house_information,
                                       'manager_boo':manager_boo,
                                       'manager_information':manager_information,
                                       'nothing_boo':nothing_boo})
            
        except :
            
            print None
            nothing_boo = True
            return render_to_response('output.html', {'nothing_boo':nothing_boo})
           
    
    
    else :
        form = UserForm()
        
        return render_to_response('register.html', {'form':form})
  
    
    
