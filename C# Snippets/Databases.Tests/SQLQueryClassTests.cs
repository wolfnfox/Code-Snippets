using System;
using System.Collections.Generic;
using Xunit;

namespace Databases.Tests
{
    public class SQLQueryClassTests
    {
        [Fact]
        public void Initialising_With_Null_String_Throws_Exception()
        {
            Assert.Throws<ArgumentNullException>(() => new SQLQuery(null));
        }

        [Fact]
        public void Initialises_With_SQL_Query_String()
        {
            string query = "Test";
            var sqlQuery = new SQLQuery(query);
            Assert.Equal(sqlQuery.sql, query);
        }

        [Fact]
        public void Equals_Returns_False_When_Comparing_SQLQuery_To_Null()
        {
            var sqlQuery = new SQLQuery("Test");
            Assert.False(Equals(sqlQuery, null));
        }

        [Fact]
        public void Equals_Returns_True_When_Comparing_SQLQuery_To_Itself()
        {
            var sqlQuery = new SQLQuery("Test");
            Assert.True(Equals(sqlQuery, sqlQuery));
        }

        [Fact]
        public void Equality_Operator_False_When_Comparing_SQLQuery_To_Null()
        {
            var sqlQuery = new SQLQuery("Test");
            Assert.False(sqlQuery == null);
        }

        [Fact]
        public void Equality_Operator_True_When_Comparing_SQLQuery_To_Itself()
        {
            var sqlQuery = new SQLQuery("Test");
#pragma warning disable CS1718 // Comparison made to same variable
            Assert.True(sqlQuery == sqlQuery);
#pragma warning restore CS1718 // Comparison made to same variable
        }

        [Fact]
        public void Inequalitys_Operator_True_When_Comparing_SQLQuery_To_Null()
        {
            var sqlQuery = new SQLQuery("Test");
            Assert.True(sqlQuery != null);
        }

        [Fact]
        public void Inequalitys_Operator_False_When_Comparing_SQLQuery_To_Itself()
        {
            var sqlQuery = new SQLQuery("Test");
#pragma warning disable CS1718 // Comparison made to same variable
            Assert.False(sqlQuery != sqlQuery);
#pragma warning restore CS1718 // Comparison made to same variable
        }
    }
}
