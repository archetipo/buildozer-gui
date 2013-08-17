#!/usr/bin/python
#-*- coding:utf-8 -*-
from lxml import etree

class Xmlloadersaver(object):
	def adjfile(self,filename):
		parser = etree.XMLParser(remove_blank_text=True)
		tree = etree.parse(filename, parser)
		fl=etree.tostring(tree,pretty_print=True,encoding='UTF-8')
		outfile=open(filename,'w')
		outfile.write(fl)
		outfile.close()
		return

	def createxmlobj(self,filename):
		self.adjfile(filename)
		in_file = open(filename,"r")
		text = in_file.read()
		in_file.close()
		return self.fromstring(text)

	def fromstring(self,text):
		return etree.fromstring(text)

	def getobjstring(self,obj):
		return etree.tostring(obj,pretty_print=True,encoding='UTF-8',xml_declaration=True)

	def savefile(self,name,stringa):
		outfile=open(name,'w')
		outfile.write(stringa)
		outfile.close()
		self.adjfile(name)
		return

class Xmloeobj(Xmlloadersaver):
	def __init__(self):
		 super(Xmlloadersaver, self).__init__()
		 self.xml=None
		 self.xmlfileout=''
		 self.xmlin=''
		 self.currpath=''
		 self.currnode=None
		 self.currtag=None
		 self.currattr=None
		 self.listattrs=[]

	def get_stringobj(self):
		return self.getobjstring(self.xml)

	def objfromFile(self,nomefile):
		self.xmlin=nomefile
		self.xmlfileout=nomefile
		self.xml=self.createxmlobj(nomefile)

	def objfromstring(self,stringa):
		self.xml=self.fromstring(stringa)

	def saveinfile(self,nomefile):
		if nomefile!='':
			self.xmlfileout=nomefile
		self.savefile(self.xmlfileout,self.getobjstring(self.xml))

	def selecttag(self,name):
		ret=False
		path='/'
		sep='/'
		for element in self.xml.iter():
			if type( element.tag ) == str:
				path+=element.tag
			if element.tag==name:
				self.currnode=element
				self.currtag=element.tag
				self.currattr=element.attrib
				self.currpath=path
				ret=True
				break
			else:
				path+=sep
		return ret

	def findpath(self,elm):
		ancora=True
		path=[]
		while ancora:
			if not elm.getparent()==None:
				path.append(elm.tag)
				elm=elm.getparent()
			else:
				path.append(elm.tag)
				ancora=False
		path.reverse()
		ret='/'
		for n in path:
			if not path.index(n)==len(path)-1:
				ret+=(n +'/')
			else:
				ret+=n
		return ret

	def FindforreplaceString(self,str_to_replace,new_string):
		ret=False
		last_tag=None
		for element in self.xml.getiterator():
			if element.tag==name and element.attrib.has_key(attr) and element.attrib[attr]==val:
				path='%s[@%s=\'%s\']'%(self.findpath(element),attr,val)
				self.currnode=element
				self.currtag=element.tag
				self.currattr=element.attrib
				self.currpath=path
				ret=True
				break
		return ret

	def selecttagwithattibname(self,name,attr,val):
		ret=False
		last_tag=None
		for element in self.xml.getiterator():
			if element.tag==name and element.attrib.has_key(attr) and element.attrib[attr]==val:
				path='%s[@%s=\'%s\']'%(self.findpath(element),attr,val)
				self.currnode=element
				self.currtag=element.tag
				self.currattr=element.attrib
				self.currpath=path
				ret=True
				break
		return ret

	def selectpos(self,attribute,val):
		ret=False
		path='/'
		sep='/'
		last_tag=None
		for element in self.xml.iter():
			if element.attrib.has_key(attribute) and element.attrib[attribute]==val:
				path='%s[@%s=\'%s\']'%(self.findpath(element),attribute,val)
				self.currnode=element
				self.currtag=element.tag
				self.currattr=element.attrib
				self.currpath=path
				ret=True
				break
		return ret

	def writeattrib(self,attr,val):
		self.currnode.attrib[attr]=val

	def writetagattrib(self,tag,attr,val):
		if self.selecttag(tag):
			self.currnode.attrib[attr]=val

	def writeStringtagattrib(self,parent,attr,val,string):
		if self.selecttagwithattibname(parent,attr,val):
			self.currnode.text=string

	def readStringtagattrib(self,parent,attr,val):
		if self.selecttagwithattibname(parent,attr,val):
			return self.currnode.text

	def writeattrib_where_attribval(self,parent,source,dest):
		attr,val=source
		if self.selecttagwithattibname(parent,attr,val):
			dattr,dval=dest
			self.currnode.attrib[dattr]=dval

	def addsettag(self,val):
		self.currnode=etree.SubElement(self.currnode, val)

	def addsettagchild(self,parent,child):
		if self.selecttag(parent):
			self.currnode=etree.SubElement(self.currnode, child)

	def writeStringCurrtag(self,string):
		self.currnode.text=string

	def getlistattributes(self):
		self.listattrs=[]
		#~ print self.currnode.tag
		for a in self.currnode.attrib:
			self.listattrs.append((a,self.currnode.attrib[a]))
		return self.listattrs

