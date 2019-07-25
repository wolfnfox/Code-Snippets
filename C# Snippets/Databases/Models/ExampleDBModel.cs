using Dapper.FluentMap.Mapping;
using System;

namespace Databases.Models
{
    public class ExampleDBModel
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public DateTime DoB { get; set; }
        public string OfficeLocation { get; set; }
        public bool CurrentlyEmployed { get; set; }
        public decimal Salary { get; set; }

        public class ExampleDBModelMap : EntityMap<ExampleDBModel>
        {
            public ExampleDBModelMap()
            {
                Map(p => p.ID).ToColumn("ID");
                Map(p => p.Name).ToColumn("Name");
                Map(p => p.DoB).ToColumn("DoB");
                Map(p => p.OfficeLocation).ToColumn("Office Location");
                Map(p => p.CurrentlyEmployed).ToColumn("Currently Employed");
                Map(p => p.Salary).ToColumn("Salary");
            }
        }
    }
}
