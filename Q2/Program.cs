using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp3
{
    internal class Program
    {
        static void Main(string[] args)
        {
            
            Console.WriteLine("Please Enter Your File Location Here:");
            string filespath = Console.ReadLine();
            string txtName=null;
            
                var lineNumber = 0;
            //Enter your SQL Server Connection
            using (SqlConnection conn = new SqlConnection(@"Data Source=DESKTOP-85P5FQN\SQLEXPRESS; Integrated Security= true"))
                {
                    conn.Open();
                   
                    string[] array = Directory.GetFiles(@filespath, "*.csv");
                    for (int i = 0; i < array.Length; i++)
                    {
                        try
                        {
                            txtName = array[i];
                            using (StreamReader reader = new StreamReader(txtName))
                            {

                                while (!reader.EndOfStream)
                                {
                                    var line = reader.ReadLine();
                                    if (lineNumber != 0)
                                    {
                                        var values = line.Split(',');

                                        var sql = "INSERT INTO CSVImport.dbo.T_SalesRecords VALUES ('" + values[0] + "','" + values[1] + "'," + values[2] + "'," + values[3] + "'," + values[4] + "'," + values[5] + "'," + values[6] + "'," + values[7] + "'," + values[8] + "'," + values[9] + "'," + values[10] + "'," + values[11] + "'," + values[12] + "'," + values[13] + ")";
                                    

                                        var cmd = new SqlCommand();
                                        cmd.CommandText = sql;
                                        cmd.CommandType = System.Data.CommandType.Text;
                                        cmd.Connection = conn;

                                        cmd.ExecuteNonQuery();
                                    }
                                    lineNumber++;
                                }
                            }
                        }
                        catch (System.Data.SqlClient.SqlException exception)
                        {
                            
                            string mydocpath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                            Console.WriteLine(exception.ToString());
                            string dir = mydocpath + @"\ERROR";
                            if (!Directory.Exists(dir))
                            {
                                Directory.CreateDirectory(dir);
                            }
                     
                        string result= Path.GetFileName(txtName);
                            File.Move(txtName, dir + "\\"+ result);
                            Console.WriteLine("Moved to Error File");
                            Console.WriteLine(txtName.ToString());
                        }
                    }
                    conn.Close();
                }
                Console.WriteLine("Products Import Complete");
            string mydocpath1 = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            string dir1 = mydocpath1 + @"\PROCESSED";
            if (!Directory.Exists(dir1))
            {
                Directory.CreateDirectory(dir1);
            }
          
            string result1 = Path.GetFileName(txtName);
            File.Move(txtName, dir1 + "\\" + result1);
            Console.WriteLine("Moved to PROCESSED File");
            Console.WriteLine(txtName.ToString());


            
        }
    }


    }




