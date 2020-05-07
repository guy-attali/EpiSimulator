# EpiSimulator
EpiSimulator is a python infrastructure to help simulate pandemic spread and test various policies effectiveness.
The main simulator component is the `World` class, which advance the world by calling `world.tick`. 
The actions in the worlds described as `procedures`.

## The entities
Brief explain of the entities:

##### Site
Represents a physical place. Each physical place should be represnted by `Site` or one of its subclasses.

##### Person
This class represents a person. In order to add  traits to a person (for example, temperature) you should add it through 
the PersonTraits class. 

#### Scenario
Represents the world layout construction. This class `build` method will create all persons, sites policies and procedures.

#### Procedure
An abstract class that represents an action. There are two types of procedures: `PersonProcedure` and `SiteProcedure`, 
each one act on the corresponding entity.
This class has two methods: 

`should_apply` - Does this procedure should be invoked?

`apply` - Invoke the action.
#### DecoratedProcedure
A class the uses to modify procedures. It receives the procedure in its c'tor, and has to implement `should_apply` and 
`apply` like any procedure.
#### Policy 
An abstract class to modify the normal advance of the world. It is done through decorating procedures, and the 
decoration happens in this class. This class methods are:

`decorate_procedure` - Will be called on every procedure. If the policy need to change some procedure action or 
invoking condition, this is the place.

`world_pretick`, `world_posttick` - will be called before/after every tick

`world_post_scenario_build` - will be called after the scenario done building.

`finish` - called at the end of the simulation. 

#### Plugin
An entity to allow data collection/output. This class has the same hooks as policy: `world_pretick`, `world_posttick`,
 `world_post_scenario_build` etc. The difference is that `Policy` take an active part and affect the flow (change procedures),
 but `Plugin` acts as an observer.

## What should I implement?
Basically, all you have to implement is your `Policy`,`Procedure` and `Scenrio` classes (make sure to inherit from
 their bases). You may also create a `Plugin` class to collect data as the program run.
 
## Running the script
 TBD
 
