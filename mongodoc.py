# MongoLib
# Simple Python object to Mongo document mapper
# Copyright Nashad Haq 2012
# Version: 0.1

import pymongo

# MongoDoc
# This is an abstract baseclass for mongo documents
# to use this abstract base class:
#   1) inherit from this class
#   2) define 'collection' class variable
#   3) define the database fields using all-caps and underscore
#      class variables and regular document/object field name
#      (ex. FIELD1 = "field1" )

class MongoDoc(object):
    
    collection = None
    OBJECT_ID = "_id"

# __init__
# Initialize a MongoDoc object setting all fields to null
#
#

    def __init__(self,d=None):
        cls = type(self)
        if d != None:
            self.fromDict(d)
            return
        for f in cls.__dict__:
            if not f.startswith('__') and f.isupper():
                docField = getattr(cls,f)
                setattr(self,docField,None)

# fromDict
# Set all the fields for the object using the input dictionary
#
#
    
    def fromDict(self,mongoDict):
        cls = type(self)   
        for f in cls.__dict__:
            if not f.startswith('__') and f.isupper():
                docField = getattr(cls,f)
                if mongoDict.has_key(docField):
                    setattr(self,docField,mongoDict[docField])
                else:
                    setattr(self,docField,None)
        if mongoDict.has_key("_id"):
            setattr(self,"_id",mongoDict["_id"])

# toDict
# Return a dictionary created from all the fields in the mongo object
#
#   
    def toDict(self):
        d = {}
        cls = type(self)
        for f in cls.__dict__:
            if not f.startswith('__') and f.isupper():
                docField = getattr(cls,f)
                if getattr(self,docField,None) != None:
                    d[docField] = getattr(self,docField)
                else:
                    d[docField] = None
        if hasattr(self,"_id"):
            d["_id"] = getattr(self,"_id")
        return d

# save
# Save the object to the database 
#   * Insert if it is a new object
#   * Update if it is an existing object
#
#
    def save(self,db):
        cls = type(self)
        colName = getattr(cls,"collection")
        coll = db[colName]
        coll.save(self.toDict())

# insert
# Insert the object into the defined collection in the database
#
#

    def insert(self,db):
        cls = type(self)
        colName = getattr(cls,"collection")
        coll = db[colName]
        if hasattr(self,"_id") == False:
            coll.insert(self.toDict())

# remove
# Remove the object from the defined collection in the database
#
#
    def remove(self,db):
        cls = type(self)
        collName = getattr(cls,"collection")
        coll = db[collName]
        if hasattr(self,"_id"):
            coll.remove({"_id":self._id})

# find_one
# Find one object in the collection meeting the key value criteria
# Return None if nothing found
#
    @classmethod
    def find_one(cls,db,**kv):
        colName = getattr(cls,"collection")
        coll = db[colName]
        item = coll.find_one(kv)        
        if item == None:
            return None
        obj = cls(item)
        return obj

# find
# Return a list of objects from the collection meeting the key value
#   criteria
#
        
    @classmethod
    def find(cls,db,**kv):
        colName = getattr(cls,"collection")
        coll = db[colName]
        items = coll.find(kv)
        objs = []
        for i in items:
            obj = cls(i)
            objs.append(obj)            
        return objs

# find_exp
# Return a list of objects from the collection meeting the query expression criteria
# Note: the expression criteria is a python dictionary using mongo semantics for querying 
    @classmethod
    def find_exp(cls,db,exp):
        colName = getattr(cls,"collection")
        coll = db[colName]
        items = coll.find(exp)
        objs = []
        for i in items:
            obj = cls(i)
            objs.append(obj)            
        return objs

# remove_exp
# Remove documents in the mongo collection meeting the criteria specified 
#   in the exp dictionary
# Note: the expression criteria is a python dictionary using mongo semantics for querying
#

    @classmethod
    def remove_exp(cls,db,exp):
        collName = getattr(cls,"collection")
        coll = db[collName]
        coll.remove(exp)
            
        
        





                
    
