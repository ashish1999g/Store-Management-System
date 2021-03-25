import sqlite3 as sq
from os import system
from tabulate import tabulate
from datetime import datetime,date


con=sq.connect("store.db")
cur=con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ITEMS(
				name varchar UNIQUE,
				cost INT NOT NULL,
				price INT NOT NULL,
				quantity INT
				);''')
cur.execute('''CREATE TABLE IF NOT EXISTS INVOICE(
				invoice_code INT PRIMARY KEY,
				-- invoice_name VARCHAR NOT NULL UNIQUE,
				invoice_date VARCHAR NOT NULL,
				amount INT NOT NULL
				);''')

class item:
	# disc/price/quantity
	# class disc:		#Discription
		# company_name/model/name
	def __init__(self,name,cost,price,quantity):
		self.name=name
		self.cost=cost
		self.price=price
		self.quantity=quantity

	def add_item(self):
		try:
			cur.execute('''INSERT INTO ITEMS VALUES(?,?,?,?)''',(self.name,self.cost,self.price,self.quantity))
		except:
			print("Error Entering values")
		con.commit()


# class customer:
	# customer name/customer mobile number/customer balance/customer address/
	# debit = db
	# credit = cr
	# def __init__(self,name,mobile,,)



if __name__=="__main__":
	while 1:
		# system('cls')
		mm=0
		print('''
			1. Stock Menu
			2. Customer Menu
			3. Ledger Menu
			4. Exit
			''')
		try :
			mm=int(input("Enter Choice:"))#mm=main menu
		except :
			print('='*10," INVALID INPUT ",'='*10)
		if mm==0:
			pass
		elif mm==1:
			while 1:
				# system('cls')
				print('''
			STOCK MENU:

			1. Add New Item
			2. Update Item Price
			3. Update Item Cost
			4. Delete Item
			5. Display Item
			6. Back to Main Menu
					''')
				sm=0	#Stock Menu
				try:
					sm=int(input("Enter Choice:"))
				except:
					print('='*10," INVALID INPUT ",'='*10)

				if sm==0:
					pass

				elif sm==1:	# add new item
					name=input('''
Enter Item Name:					
IN ORDER:
Item Name-> Company Name-> Model Name-> Specifications
		''').strip()
					quantity=int(input("Enter Quantity:"))
					cost=int(input("Enter Cost:"))
					price=int(input("Enter Price:"))
					i1=item(name,cost,price,quantity)
					i1.add_item()

				elif sm==2:	# Update item price
					name=input("Enter Name to Update:").strip()
					price=int(input("Enter New Price of Item"))
					try:
						cur.execute('UPDATE ITEMS SET Price=? WHERE name=?',(price,name))
					except Exception as e:
						print(e)
					con.commit()

				elif sm==3: # Update item Cost
					name=input("Enter Name to Update:").strip()
					cost=int(input("Enter New Cost:"))
					try:
						cur.execute("UPDATE ITEMS SET cost=? where name=?",(cost,name))
					except Exception as e:
						print(e)
					con.commit()

				elif sm==4: # Delete item
					name=input("Enter Name to delete:").strip()
					try:
						cur.execute("DELETE FROM ITEMS WHERE name=?",(name,))
					except Exception as e:
						print(e)
					con.commit()
	
				elif sm==5: # Display item
					name=input("Enter Item Name to Display:").strip()
					try:
						cur.execute('SELECT * FROM ITEMS WHERE name LIKE ?',('%'+name+'%',))
					except Exception as e:
						print(e)

					print(tabulate(cur.fetchall(),['NAME','COST','PRICE','QUANTITY'],tablefmt='pretty'))
					
				else :
					system("cls")
					break


		elif mm==2:
			print('''
			CUSTOMER MENU:

			1. Create Invoice
			2. Create Quotation	
			3. Print Invoice
			4. Print Master Invoice
			5. Back to Menu
				''')
			cm=0	#Customer Menu
			try:
				cm=int(input("ENTER CHOICE:"))
			except:
				print('='*10," INVALID INPUT ",'='*10)
			if cm==0:
				pass

			elif cm==1:
				total=0
				date=date.today()
				# iy=datetime.now().year
				cur.execute('SELECT MAX(invoice_code) FROM INVOICE')
				z=cur.fetchone()
				# iec==Invoice Code
				if z==(None,):
					iec=1
				else:
					iec=z[0]+1
				cur.execute('''CREATE TABLE IF NOT EXISTS {}(
					SN INTEGER PRIMARY KEY,
					item VARCHAR,
					quantity INT,
					price INT,
					amount INT
					)'''.format('_'+str(iec)))
				
				while 1:
					try:
						a=input('''
			-Press e to end and print.
			-Press enter to continue....
									''')
					except:
						pass
					if a =='e':
						cur.execute('INSERT INTO INVOICE VALUES (?,?,?)',(iec,date,total))
						con.commit()
						system("cls")
						print('*'*15," INVOICE ->{}".format(iec),'*'*15)
						cur.execute('SELECT * FROM {}'.format('_'+str(iec)))
						data=cur.fetchall()
						print(tabulate(data,['Serial','Item','Quantity','Price','Amount'],tablefmt='pretty'))
						print('*'*40,'Total=',total)
						break
					else:
						name=input('''
		Enter Item Name:					
		IN ORDER:
		Item Name-> Company Name-> Model Name-> Specifications
				''').strip()

						# price:
						try:
							cur.execute('SELECT price from ITEMS WHERE name=?',(name,))
							price=int(cur.fetchone()[0])
						except:
							price=int(input("Enter Price:"))

						q=int(input("Enter Quantity:"))
						cur.execute('SELECT quantity from ITEMS WHERE name=?',(name,))
						qq=cur.fetchone()
						try:
							if q>qq[0]:
								print("INSUFFICIENT QUANTITY AVAILABLE")
								q=qq[0]
							cur.execute('UPDATE ITEMS SET quantity=? WHERE name=?',(qq[0]-q,name))
						except:
							pass							
						
						amount=price*q
						total+=amount
						cur.execute('''INSERT INTO {} (item,quantity,price,amount) VALUES(?,?,?,?)'''.format('_'+str(iec)),(name,q,price,amount))
						con.commit()

			elif cm==2:
				total=0
				# date=date.today()
				# iy=datetime.now().year
				# cur.execute('SELECT MAX(invoice_code) FROM INVOICE')
				# iec==Invoice Code
				# iec=int(cur.fetchone())+1
				cur.execute('''CREATE TABLE IF NOT EXISTS QUOTATION(
					SN INTEGER PRIMARY KEY,
					item VARCHAR,
					quantity INT,
					price INT
					);''')
				
				while 1:
					try:
						a=input('''
			-Press e to end and print.
			-Press enter to continue....
									''')
					except:
						pass
					if a=='e':
						# cur.execute('INSERT INTO QUOTATION VALUES (?,?,?)',(iec,date,total))
						# con.commit()
						system("cls")
						print('*'*15," QUOTATION ",'*'*15)
						cur.execute('SELECT * FROM QUOTATION')
						data=cur.fetchall()
						print(tabulate(data,['Serial','Item','Quantity','Price'],tablefmt='pretty'))
						break
					else:
						name=input('''
		Enter Item Name:					
		IN ORDER:
		Item Name-> Company Name-> Model Name-> Specifications
				''').strip()

						# price:
						try:
							price=input("Enter Price:")
						except:
							cur.execute('SELECT price from ITEMS WHERE name=?',(name,))
							price=int(cur.fetchone()[0])
						
						q=int(input("Enter Quantity:"))
						cur.execute('SELECT quantity from ITEMS WHERE name=?',(name,))
						qq=cur.fetchone()
						if q>qq:
							print("INSUFFICIENT QUANTITY AVAILABLE")
							q=qq
						cur.execute('''INSERT INTO QUOTATION VALUES(?,?,?)''',(name,q,price))
						con.commit()



			elif cm==3:
				iec=int(input("Enter Invoice Number:"))
				try:
					cur.execute('SELECT * FROM {}'.format('_'+str(iec)))
				except :
					print("Invoice Not Exist")

				data=cur.fetchall()
				print('*'*15," INVOICE ->{}".format(iec),'*'*15)
				print(tabulate(data,['Serial','Item','Quantity','Price'],tablefmt='pretty'))

			elif cm==4:
				cur.execute('SELECT * FROM INVOICE')
				data=cur.fetchall()
				print(tabulate(data,['Invoice Code','Invice Date','Amount'],tablefmt='pretty'))
			elif cm==5:
				# system("cls")
				break
			else:
				print('='*10,"Wrong input",'='*10)

		elif mm==3:
				print('''
			LEDGER MENU

			1. Print Ledger 
			2. Payment Submission
			3. Customer Master
			3. Check Last Balance
			4. Back to Customer Menu
					''')
				# lm=input('Enter Choice ')
		elif mm==4:
			break
		else:
			print('='*10,"Wrong input",'='*10)

con.commit()
con.close()