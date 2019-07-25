using System;
using Xunit;

namespace Helpers.Tests
{
    public class HashCodeGeneratorTests
    {
        [Theory]
        [InlineData(null,17*31)]
        public void HashCodeGenerator_Returns_0_For_Null(object TObject, int hashCode)
        {
            Assert.Equal(HashCodeGenerator.StartHash().Hash(TObject), hashCode);
        }
    }
}
