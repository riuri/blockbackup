#!/usr/bin/env python3

def aread():
	with open('block', 'rb') as i:
		count = 0
		b1 = i.read(512)
		while(b1):
			print(count)
			print(b1)
			count += 1
			b1 = i.read(512)

if __name__ == '__main__':
	print('Hello')
	aread()
