#!/usr/bin/python3

import sys
import time
import random



max_chars_before_seeing_mistake=3 # max chars before noticing a mistake
a_mistake_every_n_chars=[2,30] # how often will we have a mistake (unless the mistake isn't possible, if the char isn't on the keyboard

key_mistake=2 # max shift between wanted key and actual key on the keyboard
row_mistake=10 # one change out of n
shift_mistake=3 # one change out of n

#----


keyb=[[[0] for i in range(0,2)] for j in range(0,4)]
keyb[0][0]='1234567890-+'
keyb[0][1]='!@#$%^&*()_+'
keyb[1][0]='qwertyuiop[]'
keyb[1][1]='QWERTYUIOP{}'
keyb[2][0]="asdfghjkl;'"
keyb[2][1]='ASDFGHJKL:"'
keyb[3][0]='zxcvbnm,./'
keyb[3][1]='ZXCVBNM<>?'

long_pause=1
short_pause=0


debug=False
	

def pause(type_pause=long_pause):
	if long_pause:
		a=(random.randrange(0,100)+100)/1000
	else:
		a=(random.randrange(0,50)+40)/1000
	if not debug:
		time.sleep(a)

def typo(char):
	found=False
	for row in range(0, len(keyb)):
		for shift in range(0, len(keyb[row])):
			if char in keyb[row][shift]:
				found=True
				break
		if found==True:
			break

	if found==True:
		index=keyb[row][shift].index(char)

		new_row=row
		new_shift=shift
		new_index=index

		if random.randrange(0, row_mistake)==1: # sometimes, we it the wrong row
			if row==0:
				new_row=1
			else:
				if row==3:
					new_row=2
				else: 
					shift_row=([-1,1][random.randrange(0,2)])
					new_row=shift_row+row
			if new_index>len(keyb[new_row][new_shift])-1: # not all rows have the same size
				new_index=len(keyb[new_row][new_shift])-1

		else: 
			if (random.randrange(0,shift_mistake)==1) and (shift==1): # if not row mistake, then one change out of 2 he missed the shift
				new_shift=0 
			else:
				new_index=index
				while new_index==index:
					shift_index=random.randrange(1,key_mistake+1) * ([-1,1][random.randrange(0,2)])
					new_index=shift_index+index
					if new_index<0:
						new_index=0
					if new_index>len(keyb[new_row][new_shift])-1:
						new_index=len(keyb[new_row][new_shift])-1
		

#global max check, because not all rows have the same size
		return keyb[new_row][new_shift][new_index]
	else:
		return None
			
def add_revert(count):
	s=''
	for i in range(0,count):
		if debug:
			s=s+'-'
		else:
			s=s+'\b'
	return s


def add_mistakes(string):
	n=random.randrange(a_mistake_every_n_chars[0], a_mistake_every_n_chars[1])
	errs=[]
	while n < len(string):
		errs.append(n) 
		n=n+max_chars_before_seeing_mistake+random.randrange(a_mistake_every_n_chars[0], a_mistake_every_n_chars[1]) 
	found=False
	
	err_log=''
	for err in errs: 
		if random.randrange(0,3)==0: #one chance out of 3 to just miss a key
			l=random.randrange(0, max_chars_before_seeing_mistake+1)
			s=string[err+1:err+1+l]
			s=s+add_revert(len(s))
			string=string[0:err]+s+string[err:]
			err_log=err_log+'1'
		else: 
			s=typo(string[err])
			if s==string[err]:
				raise Exception('%s, %s what ?' % (s, string[err]))
			if s != None:
				l=random.randrange(0, max_chars_before_seeing_mistake+1)
				if l > len(string)-err:
					l=len(string)-err
# type one typo
				a=random.randrange(0,3)
				if a==0: # typed wrong letter
					s=s+string[err+1:err+1+l]
					s=s+add_revert(len(s))
					string=string[0:err]+s+string[err:]
					err_log=err_log+'2'
				if a==1:
					s=string[err]+s+string[err+1:err+1+l]
					s=s+add_revert(len(s)-1)
					string=string[0:err]+s+string[err+1:]
					err_log=err_log+'3'
				if a==2:
					s=s+string[err]+string[err+1:err+1+l]
					s=s+add_revert(len(s))
					string=string[0:err]+s+string[err:]
				err_log=err_log+'3'

	return string 

for line in sys.stdin:
	line=add_mistakes(line.strip())
	for letter in line: 
		if letter=='\b':
			sys.stdout.write('\033[1D \033[1D')
			sys.stdout.flush()
			pause()
		else:
			sys.stdout.write(letter)
			sys.stdout.flush()
			pause()
	print('')

