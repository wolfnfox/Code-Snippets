using System;
using System.Collections.Generic;

namespace Helpers
{
    /// <summary>
    /// Static class for generating Hashes of complex <see cref="Type"/>s.
    /// </summary>
    public static class HashCodeGenerator
    {
        public static int prime { get; set; } = 17;
        public static int multiplier { get; set; } = 31;

        /// <summary>
        /// <para>Initializes the <see cref="HashCodeGenerator"/> parameters.</para>
        /// <para>Should be called first before using <see cref="HashCodeGenerator.Hash"/>.</para>
        /// </summary>
        /// <param name="prime"></param>
        /// <param name="multiplier"></param>
        /// <returns></returns>
        public static int StartHash(int prime = 17, int multiplier = 31)
        {
            HashCodeGenerator.prime = prime;
            HashCodeGenerator.multiplier = multiplier;
            return prime;
        }

        /// <summary>
        /// Extension method for <see cref="Type"/> <see cref="int"/> to generate a Hash of the input <see cref="object"/> of <see cref="Type"/> T.
        /// </summary>
        /// <typeparam name="T">The type of input <see cref="object"/>.</typeparam>
        public static int Hash<T>(this int hash, T TObject)
        {
            var objectHash = EqualityComparer<T>.Default.GetHashCode(TObject);
            return unchecked((hash * multiplier) + objectHash); ;
        }
    }
}
