# 2. Abandon dataclasses to enhance entity hermetization

Date: 2023-08-03

## Status

Accepted

## Context

Our current implementation uses Python's dataclasses for domain entities. These dataclasses directly expose the fields which map to the database columns, allowing them to be manipulated directly. This makes our entities prone to invalid state changes that could violate the integrity of our domain.

In our strive to better adhere to the principles of Domain-Driven Design (DDD) and Encapsulation, we are considering replacing these dataclasses with pure Python classes, where the fields would be private and can only be modified through methods that represent domain operations.

## Decision

We will replace dataclasses with pure Python classes for our domain entities.

In these new classes, we will:

Make all fields that map to database columns private.
Provide methods that represent domain operations for all modifications of these fields.
Ensure these methods enforce all necessary business rules and invariants.
This approach aligns more closely with the principles of DDD, specifically:

* **Ubiquitous Language**: By providing methods that represent domain operations for modifying fields, we emphasize the language of our domain in our code.
* **Encapsulation**: By making fields private, we prevent external code from putting our entities into an invalid state. We can ensure that all changes to the entity's state are valid according to our business rules.
Our ORM, SQLAlchemy, supports this approach through its "classical mapping" style, which allows for a clear separation between domain models (entities) and persistence models.

## Consequences

* **Positive**: Our domain entities will better encapsulate their state, ensuring data integrity and consistency.
* **Positive**: Our code will better reflect our Ubiquitous Language, improving understandability and maintainability.
* **Negative**: We will need to update all existing code that interacts with our entities to use the new methods instead of directly modifying fields.
* **Negative**: There will be an increase in the amount of code we need to write and maintain (i.e., methods for all field modifications).

