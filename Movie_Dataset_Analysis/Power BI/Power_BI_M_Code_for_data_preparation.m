let
    Source = Csv.Document(File.Contents("C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\cars_2010_2020.csv"),[Delimiter=",", Columns=6, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Make", type text}, {"Model", type text}, {"Year", Int64.Type}, {"Engine Size (L)", type number}, {"Fuel Type", type text}, {"Price (USD)", type number}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Price (INR)", each [#"Price (USD)"]*83.5),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Make", "Maker"}})
in
    #"Renamed Columns"