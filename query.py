PRODUCT_QUERY =   """
                    SELECT {top} ProductID, Name, ProductNumber, StandardCost, ListPrice, ProductModelID, ProductCategoryID, SellStartDate, SellEndDate
                    FROM SalesLT.Product
                    {condition}
                    """

TOP_Profitable_PRODUCT =  """
                            SELECT {top}
                                ProductID,
                                Name,
                                StandardCost,
                                ListPrice,
                                ListPrice - StandardCost AS Profit
                            FROM SalesLT.Product
                            ORDER BY Profit DESC
                            """

TOP_SALES_CUSTOMER_CITY =    """
                                WITH SalesPrice AS (
                                    SELECT SalesOrderID, LineTotal
                                    FROM [SalesLT].[SalesOrderDetail]
                                ), SalesHeader AS (
                                    SELECT SalesOrderID, ShipToAddressID
                                    FROM [SalesLT].[SalesOrderHeader]
                                ), SalesAddress AS (
                                    SELECT AddressID, City
                                    FROM [SalesLT].[Address]
                                )

                                SELECT {top} SalesAddress.City, SUM(SalesPrice.LineTotal) AS TotalSales
                                FROM SalesPrice
                                    INNER JOIN SalesHeader
                                    ON SalesPrice.SalesOrderID = SalesHeader.SalesOrderID
                                    INNER JOIN SalesAddress
                                    ON SalesHeader.ShipToAddressID = SalesAddress.AddressID
                                GROUP BY SalesAddress.City
                                ORDER BY TotalSales DESC
                                """

TOTAL_SALES_CUSTOMER_GENDER =   """
                                WITH SalesPrice AS (
                                    SELECT SalesOrderID, LineTotal
                                    FROM [SalesLT].[SalesOrderDetail]
                                ), SalesHeader AS (
                                    SELECT SalesOrderID, CustomerID
                                    FROM [SalesLT].[SalesOrderHeader]
                                ), CustomerTitle AS (
                                    SELECT CustomerID, Title
                                    FROM [SalesLT].[Customer]
                                ), CustomerTitleSales AS (
                                    SELECT Title, SUM(SalesPrice.LineTotal) AS TotalSales
                                    FROM SalesPrice
                                        INNER JOIN SalesHeader
                                        ON SalesPrice.SalesOrderID = SalesHeader.SalesOrderID
                                        INNER JOIN CustomerTitle
                                        ON SalesHeader.CustomerID = CustomerTitle.CustomerID
                                    GROUP BY CustomerTitle.Title
                                )

                                (
                                SELECT 'Male', SUM(TotalSales)
                                FROM CustomerTitleSales
                                WHERE Title IN ('Mr.', 'Sr.')
                                )
                                UNION
                                (
                                SELECT 'Female', SUM(TotalSales)
                                FROM CustomerTitleSales
                                WHERE Title IN ('Ms.', 'Sra.')
                                )
                                """

TOTAL_SALES_BY_MONTH =  """
                        WITH FormattedDate AS (
                            SELECT LineTotal, FORMAT(ModifiedDate, 'yyyy-MM') AS SalesMonth
                            FROM [SalesLT].[SalesOrderDetail]
                        )

                        SELECT SalesMonth, SUM(LineTotal) AS TotalSales
                        FROM FormattedDate
                        GROUP BY SalesMonth
                        """

TOTAL_SALES_QUANTITY_BY_PRODUCT_CATEGORY =  """
                                            WITH SimplifiedSales AS (
                                                SELECT ProductID, OrderQty, LineTotal
                                                FROM [SalesLT].[SalesOrderDetail]
                                            ), SimplifiedProduct AS (
                                                SELECT ProductID, ProductCategoryID
                                                FROM [SalesLT].[Product]
                                            ), SimplifiedCategory AS (
                                                SELECT ProductCategoryID, Name AS Category
                                                FROM [SalesLT].[ProductCategory]
                                            )

                                            SELECT sc.Category, SUM(ss.OrderQty) AS SalesQuantity, SUM(ss.LineTotal) AS TotalSales
                                            FROM SimplifiedSales AS ss
                                                INNER JOIN SimplifiedProduct AS sp
                                                    ON ss.ProductID = sp.ProductID
                                                INNER JOIN SimplifiedCategory AS sc
                                                    ON sp.ProductCategoryID = sc.ProductCategoryID 
                                            GROUP BY sc.Category
                                            """