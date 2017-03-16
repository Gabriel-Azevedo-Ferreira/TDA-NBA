# TDA

In this work, we analyzed the statistics from the 2015-2016 NBA season using well-known
algorithms and topological algorithms, inspired by the work of M. Alagappan. We first
used traditional algorithms to understand the general properties of the data, as well as the
strength of the actual field positions as determinants of playing styles, and then proceeded to
a more complex abstraction given by the Mapper algorithm, implemented in the R package
TDAmapper.

By analyzing the topological structure of the data returned by the Mapper algorithm and
comparing it to the structure obtained in Alagappan’s work, we could capture a more comprehensive
understanding of playing-styles. By identifying the majority of the field positions that
were defined in his paper, we empirically proved the robustness of the Mapper algorithm, as
we used a more recent dataset from five years later than his.
