# -*- coding: utf-8 -*-
from __future__ import unicode_literals


#Django imports
from django.http import HttpResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#Django api rest 
from rest_framework import status
from rest_framework.response import Response


#Python imports
import requests

#Models 
from .models import pokemon


def chain(request, id ):
    """fetch and store pokemon from pokeapi 
    """
    response= requests.get('https://pokeapi.co/api/v2/evolution-chain/'+ str(id) +"/")
    data = response.json()

    #Get pokemon name
    try:
        evolves_to=data[u'chain']["evolves_to"] 
        
        #save chan pokemon as list 
        flag= True
        chainlist= []
        chainlist.append([data[u'chain'][u"species"]["name"]])
        while(flag == True):
            if (evolves_to==[]):
                flag=False
            else :
                aux= []              
                for i in evolves_to:
                    name =   i[u'species'][u'name']
                    aux.append(name)
                    evolves_to=i[u"evolves_to"]
                chainlist.append(aux)

        #save pokemon list
        save_pokemon(chainlist[0][0])
        for i in range(1, len(chainlist)):
      
            for j in chainlist[i]:
                save_pokemon(j)
                save_pokemon(j,Prevolution=chainlist[i-1][0])
                save_pokemon(chainlist[i-1][0], Evolution=j)
                try:
                    save_pokemon(j, Evolution=chainlist[i+1][0])
                except IndexError:
                    pass


    except IntegrityError :
        return HttpResponse("<h1>Chain Pokemon is already saved<h1>")
    
        
    return HttpResponse("<h1>Chain Pokemon save<h1>")
    

def save_pokemon(name,  Prevolution= None, Evolution= None):
    """save pokemon data
    """ 
    
    #found Pokemon from name
    response= requests.get('https://pokeapi.co/api/v2/pokemon/' + name + '/' )
    data=response.json()
    
    Pokemon= pokemon()
    Pokemon.name=name
    Pokemon.idApi=int(data[u'id'])
    Pokemon.height=data[u'height']
    Pokemon.weight=data[u'weight']
    stat=[]
    for i in data[u'stats']:
        stat.append(i[u'base_stat'])

    Pokemon.speed= stat[0]
    Pokemon.specialDefense =stat[1]
    Pokemon.specialAttack =stat[2]
    Pokemon.defense = stat[3]
    Pokemon.attack = stat[4]
    Pokemon.hp = stat[5]

    #chain Evolution 
    if Prevolution is not None:
        Pokemon= pokemon.objects.get(name= name)
        Pokemon.prevolution=Prevolution 
        Pokemon.save()
    if Evolution is not None:        
        Pokemon= pokemon.objects.get(name= name)
        
        if Pokemon.evolution != Evolution and Pokemon.evolution!=None: 
            Pokemon.evolution= str(Pokemon.evolution)+','+str(Evolution)
        else:        
            Pokemon.evolution= Evolution
        
        Pokemon.save()
        
    Pokemon.save()

    pass    



def list_pokemon_name(request, name):
    """found pokemon from name and show data
    """
    
    
    try:
        data = pokemon.objects.get(name = name)
        prevolution= []
        if data.prevolution != None:
            prevolutions=data.prevolution.split(",")
            for i in prevolutions:
                prevolution.append(pokemon.objects.get(name=i))

        evolution=[]
        if data.evolution != None:
            evolutions = data.evolution.split(",")
            for i in evolutions:
                evolution.append(pokemon.objects.get(name=i))
                
        return render(request, 'pokemon/index.html' ,{'p_data': data,"prevolution":prevolution, "evolution": evolution})
    except ObjectDoesNotExist:
        return HttpResponse("<h1> pokemon not exist <h1>")

  
