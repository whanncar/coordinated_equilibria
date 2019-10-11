# coordinated_equilibria


## TODO

* Make tests for everything

* Decide on and implement algorithm for finding vertices

* ~~Implement algorithm for finding C~~

* Implement algorithm for finding D




## Documentation



### Basic objects


#### NFG

* Attributes
  * players
  * actions
  * states
  * payoffs
* Methods
  * get_payoffs


#### Node

* Attributes
  * player
  * action
  * children


#### Plan

* Attributes
  * state
  * root
* Methods
  * get_on_path_action_profile
  * get_copy
  * get_deviation_payoffs



### LP


#### LP

* prepare_LP_data
* get_all_vertices


#### LP_wrapper

* minimize_container
* maximize_container
* maximize_with_probs_container
* maximize


### Equilibrium set calculators


#### coord_eq

* get_coord_eq_set


#### self_contained

* get_self_contained_set
* get_self_contained_labels


#### pbe

* get_pbe_set
* get_pbe_labels



### Helpers


#### construction

* make_plans
* make_plans_with_given_labels
* make_plans_for_given_state_with_given_labels


#### utils

* get_ordered_tuples



### IO/UI


#### file_io

* load_NFG
* save_NFG













