"""

- Full Address column has zip codes that are at the beginning of the string.

- In the Fuel Type column, liquid natural gas has multiple different names such as, “lng”, “LNG”, “liquid natural gas”, “liquified natural gas”, and “liquefied natural gas”.

- Values inside the Site ID column are a mixture of strings and integers depending on the Site Name. This could cause problems when trying to query by Site ID as a whole. 

- The Date & Time column does not use military time, am., or pm., so there is no way to distinguish whether it is before or after noon. 

"""