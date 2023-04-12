# payment-system
Payment system implemented by an aws state machine

The purpose of the project is not 
- Data access should be done by means of a Rest API, GRAPHQL or any other third party style but data should not <br> be access directly form the lambdas by Pymongo. <br> we 
- Data handlers are repeated, this should be made a third party library and deployed to AWS code artifact.
- 