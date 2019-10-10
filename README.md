# coordinated_equilibria

* Make objects
  * ~~Normal Form Game~~
  * ~~Node~~
  * ~~Plan~~

* Make construction code
  * ~~construction~~

* Make LP classes (?)

* Make tests for everything

* ~~Restore understanding of algorithm~~

* Decide on and implement algorithm for finding vertices



### coord_eq

* get_coord_eq_set



### self_contained

* get_self_contained_set
* get_self_contained_labels



### pbe

* get_pbe_set
* get_pbe_labels








### file_io

* load_NFG
* save_NFG



### construction

* make_plans
* make_plans_with_given_labels
* make_plans_for_given_state_with_given_labels


### utils

* get_ordered_tuples






### NFG

* Attributes
  * players
  * actions
  * states
  * payoffs
* Methods
  * get_payoffs


### Node

* Attributes
  * player
  * action
  * children


### Plan

* Attributes
  * state
  * root
* Methods
  * get_on_path_action_profile
  * get_copy
  * get_deviation_payoffs
