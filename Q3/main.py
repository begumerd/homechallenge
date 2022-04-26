import pyodbc
#Connection SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-85P5FQN\SQLEXPRESS;'
                      'Database=AdventureWorks2019;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
#Create Fact.Sales Table
cursor.execute('''
		CREATE TABLE Sales.FactSales (
			SalesOrderDetailKey int PRIMARY KEY,
	SalesOrderKey INT NOT NULL,
	ProductKey INT NOT NULL,
	SpecialOfferKey INT NOT NULL,
	SalesOrderStatusKey INT NOT NULL,
	SalesOnlineOrderFlagKey INT NOT NULL,
	SalesOrderAccountNumber nvarchar(16) NOT NULL,
	SalesOrderCustomerKey INT NOT NULL,
	SalesPersonKey INT NOT NULL,
	TerritoryKey INT NOT NULL,
	BillToAddressKey INT NOT NULL,
	ShipToAddressKey INT NOT NULL,
	ShipMethodKey INT NOT NULL,
	SalesOrderDetailModifiedDateKey INT NOT NULL,
	SalesOrderDateKey INT NOT NULL,
	SalesOrderDueDateKey INT NOT NULL,
	SalesOrderShipDateKey INT NOT NULL,
	SalesOrderModifiedDateKey INT NOT NULL,
	OrderQty INT NOT NULL,
	UnitPrice MONEY NOT NULL,
	UnitPriceDiscount MONEY NOT NULL,
	LineTotal MONEY NOT NULL,
	SalesOrderSubTotal MONEY NOT NULL,
	SalesOrderTaxAmount MONEY NOT NULL,
	SalesOrderFreighAmount MONEY NOT NULL,
	SalesOrderTotalDueAmount MONEY NOT NULL
			)'''
               )

#Populate Fact.Sales Table
cursor.execute('''
		INSERT INTO Sales.FactSales  (SalesOrderDetailKey,SalesOrderKey, ProductKey,SpecialOfferKey, SalesOrderStatusKey, SalesOnlineOrderFlagKey, SalesOrderAccountNumber, SalesOrderCustomerKey, SalesPersonKey, TerritoryKey, BillToAddressKey, ShipToAddressKey, ShipMethodKey, SalesOrderDetailModifiedDateKey, SalesOrderDateKey, SalesOrderDueDateKey, SalesOrderShipDateKey, SalesOrderModifiedDateKey, OrderQty, UnitPrice, UnitPriceDiscount, LineTotal, SalesOrderSubTotal,SalesOrderTaxAmount,SalesOrderFreighAmount ,SalesOrderTotalDueAmount  	)
		SELECT top 100 
SOD.SalesOrderDetailID AS SalesOrderDetailKey,
SOH.SalesOrderID AS SalesOrderKey,
SOD.ProductID AS ProductKey,
SOD.SpecialOfferID AS SpecialOfferKey,
SOH.Status AS SalesOrderStatusKey,
SOH.OnlineOrderFlag AS SalesOnlineOrderFlag,
SOH.AccountNumber AS SalesOrderAccountNumber,
SOH.CustomerID AS SalesOrderCustomerKey,
ISNULL(SOH.SalesPersonID,0) AS SalesPersonKey,
SOH.TerritoryID AS TerritoryKey,
SOH.BillToAddressID AS BillToAddressKey,
SOH.ShipToAddressID AS SOHipToAddressKey,
SOH.SHipMethodID AS SOHipMethodKey,
CONVERT(INT, CONVERT(VARCHAR(8),SOD.ModifiedDate,112)) AS SalesOrderDetailModifiedDateKey,
CONVERT(INT, CONVERT(VARCHAR(8),SOH.OrderDate,112)) AS SalesOrderDateKey,
CONVERT(INT, CONVERT(VARCHAR(8),SOH.DueDate,112)) AS SalesOrderDueDateKey,
CONVERT(INT, CONVERT(VARCHAR(8),SOH.SHipDate,112)) AS SalesOrderSHipDateKey,
CONVERT(INT, CONVERT(VARCHAR(8),SOH.ModifiedDate,112)) AS SalesOrderModifiedDateKey,
SOD.OrderQty,
SOD.UnitPrice,
SOD.UnitPriceDiscount,
SOD.LineTotal,
SOH.SubTotal AS SalesOrderSubTotal,
SOH.TaxAmt AS SalesOrderTaxAmount,
SOH.Freight AS SalesOrderFreightAmount,
SOH.TotalDue AS SalesOrderTotalDueAmount
FROM Sales.SalesOrderDetail SOD
	LEFT JOIN Sales.SalesOrderHeader SOH ON SOD.SalesOrderID = SOH.SalesOrderID  
               ''' )
#Create Dim.Customer Table
cursor.execute('''
		CREATE TABLE Sales.DimCustomer (
		BusinessEntityID INT PRIMARY KEY,
	PersonType nchar(2) NOT NULL,
	NameStyle nvarchar(16) NOT NULL,
	Title nvarchar(8) NULL,
	FirstName nvarchar(16)  NOT NULL,
	MiddleName nvarchar(16)  NULL,
	LastName nvarchar(16)  NOT NULL,
	PersonID INT  NULL,
	AddressLine1 nvarchar(60) NOT NULL,
	AddressLine2 nvarchar(60)  NULL,
	City nvarchar(30) NOT NULL,
	PostalCode nvarchar(15) NOT NULL,
	StateProvinceName  nvarchar(60) NOT NULL,
	AdressTypeName nvarchar(30) NOT NULL,
	ContactTypeName nvarchar(30) NOT NULL,
	EmailAddress nvarchar(50)  NULL,
	PhoneNumber nvarchar(50) NOT NULL,
	PhoneNumberTypeName nvarchar(30) NOT NULL,
	CountryRegionName nvarchar(30) NOT NULL,
	CustomerID INT NOT NULL,
	CustomerModifiedDateKey INT NOT NULL
	)'''
               )

#Populate Dim.Customer Table
cursor.execute('''
		INSERT INTO Sales.DimCustomer (BusinessEntityID ,PersonType	,
NameStyle	,
Title	,
FirstName	,
MiddleName	,
LastName	,
PersonID	,
AddressLine1	,
AddressLine2	,
City	,
PostalCode	,
StateProvinceName	,
AdressTypeName	,
ContactTypeName	,
EmailAddress	,
PhoneNumber	,
PhoneNumberTypeName	,
CountryRegionName	,
CustomerID,
CustomerModifiedDateKey
)
		select  top 100 persondetail.*,  ISNULL(Sales.Customer.CustomerID,0) CustomerID, 
CONVERT(INT, CONVERT(VARCHAR(8),Sales.Customer.ModifiedDate,112)) AS CustomerModifiedDateKey

  from Sales.Customer 
inner join
(
select  person.Person.BusinessEntityID,
ISNULL(person.Person.PersonType,'') PersonType,ISNULL(person.Person.NameStyle,'') NameStyle,
ISNULL(person.Person.Title,'') Title,ISNULL(person.Person.FirstName,'') FirstName,
ISNULL(person.Person.MiddleName,'') MiddleName,ISNULL(person.Person.LastName,'') LastName,
ISNULL(person.BusinessEntityContact.PersonID,0) PersonID,ISNULL(person.Address.AddressLine1,'') AddressLine1,
ISNULL(Address.AddressLine2 ,'') AddressLine2,ISNULL(Address.City,'') City,
ISNULL(Address.PostalCode,'') PostalCode,ISNULL(person.StateProvince.Name,'') as StateProvinceName ,
ISNULL(AddressType.Name,'') as adrestypename,
ISNULL(person.ContactType.Name,'') as contactTypeName,ISNULL(person.EmailAddress .EmailAddress,'') EmailAddress,
ISNULL(person.PersonPhone.PhoneNumber ,'') PhoneNumber,ISNULL(Person.PhoneNumberType.Name,'') as PhoneNumberTypeName,
ISNULL(person.CountryRegion.Name,'') as CountryRegionName
from
 person.BusinessEntity 
left join person.BusinessEntityContact on person.BusinessEntityContact.BusinessEntityID=person.BusinessEntity.BusinessEntityID
left join person.Person on person.BusinessEntity.BusinessEntityID=person.Person.BusinessEntityID
left join person.ContactType on ContactType.ContactTypeID=BusinessEntityContact.ContactTypeID
left join person.BusinessEntityAddress on  BusinessEntityAddress.BusinessEntityID=person.BusinessEntity.BusinessEntityID
left join Person.Address on person.BusinessEntityAddress.AddressID=Person.Address.AddressID
left join Person.AddressType on person.BusinessEntityAddress.AddressTypeID=Person.AddressType.AddressTypeID
left join  person.EmailAddress on  person.EmailAddress.BusinessEntityID=person.BusinessEntity.BusinessEntityID
left join person.PersonPhone on person.PersonPhone.BusinessEntityID=person.BusinessEntity.BusinessEntityID
left join Person.PhoneNumberType on Person.PhoneNumberType.PhoneNumberTypeID=person.PersonPhone.PhoneNumberTypeID
left join person.StateProvince on  person.StateProvince.StateProvinceID=Address.StateProvinceID
left join person.CountryRegion on person.CountryRegion.CountryRegionCode=person.StateProvince.CountryRegionCode
)persondetail on Sales.Customer.PersonID=persondetail.BusinessEntityID  
               ''' )
conn.commit()


