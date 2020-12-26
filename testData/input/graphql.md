---
title: "Graphql"
date: "2020-12-25T08:45:46"
description: "Anki deck for Graphql cards."
draft: true
# image: /path/to/image
---

# Graphql

## What is the syntax for passing arguments to fields in Graphql?

Use parentheses after the field name with a comma separated list of names followed by a colon and a value.
These arguments are unordered.

```graphql
{
  user(id: 4) {
    id
    name
    profilePic(width: 100, height: 50)
  }
}
```

## What are the three types of operations allowed in Graphql?

- _query_ – a read‐only fetch.
- _mutation_ – a write followed by a fetch.
- _subscription_ – a long‐lived request that fetches data in response to source events.

## Describe the building blocks of a basic graphql query operation

```graphql
# the query operation with variables
query queryName(variable: VariableType) {
  # the selection set

  # a field in the selection set with an argument
  field(argument: ArgumentValue) {

    # a field alias and a nested field in the selection set
    fieldAlias: NestedField

  }
}
```

## What is the purpose of a fragment in graphql?

A fragment allows for reuse of common selections of fields.

For example this fragment selects the id, name, and profile picture on the user field.

```graphql
query withFragments {
  user(id: 4) {
    friends(first: 10) {
      ...friendFields
    }
    mutualFriends(first: 10) {
      ...friendFields
    }
  }
}

fragment friendFields on User {
  id
  name
  profilePic(size: 50)
}
```

## What is a type condition of a fragment in graphql?

When you define a fragment you specify the name and the type the fragment is defined for.

```graphql
# name pageFragment
# defined on type Page
fragment pageFragment on Page {

}
```

The selection defined by a fragment will only return values when the object the fragment is operating on matches the type the fragment applies to.

## What is the syntax used to define inline fragments in graphql?

Use `...` followed by `on Type` and then the selection in brackets.

```graphql
user {
  follows {
    ... on User {
      name
    }
    ... on Page {
      title
    }
  }
}
```

## Why would you use inline fragments in graphql?

In order to conditionally select fields based on the object the fragment is operating on.

Fragment selections are only defined when the object the fragment is operating on matches the type the fragment applies to.

Consider the following query.

```graphql
user {
  follows {
    ... on User {
      name
    }
    ... on Page {
      title
    }
  }
}
```

The user may follow other users and pages.
When the user follows a page the inline fragment for Page is defined and we get the title of the page.
When the user follows another User the user fragment is applied and we get the name of the followed user.

## How are variables passed to a graphql query?

Variables are provided at the top of an operation and are in scope throughout the operation.

```graphql
query getUser($name: String) {
  user(name: $name) {
    id
  }
}
```

## What is the scope of variables in a graphql operation?

Variables have a global scope within a graphql operation.
Variables can be accessed within fragments as long as the variable is defined in the top level the operation the fragment is operating on and the variable has the same name.

## How are default values given to variables in graphql queries?

Using the syntax `Variable: Type = DefaultValue`

Here is an example of giving the variable `$id` a default value of `0`.

```graphql
query getUser($id: Int = 0) {
  user(id: $id) {
    name
  }
}
```

## What are the two directives supported by any spec compliant graphql server?

- `@include(if: Boolean)` Only include this field in the result if the argument is `true`.
- `@skip(if: Boolean)` Skip this field if the argument is `true`.

## Give an example of using the @include directive in graphql

The directive comes after arguments.

```graphql
query profile($withMyInfo: Boolean!) {
  me: user(id: $id) @include(if: $withMyInfo) {
    id
    name
    email
  }
}
```

The directive is often used with variables to the query.

```graphql
query UserInfo($id: Int, $withFriends: Boolean!) {
  user(id: $id) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}
```

## What are the built in Scalar types in graphql?

- _Int_ - represents a 32 bit signed integer
- _Float_ - represents a signed double
- _String_ - represents utf-8 text data
- _Boolean_ - represents true or false. Uses booleans if supported else integers 1 and 0.
- _ID_ - represents a unique identifier. Used as keys, must be serializable to a string but can be a numeric value.

## How are non-null and nullable fields specified in graphql?

Non null fields are specified by adding a trailing exclamation mark after the type.

```graphql
name: String!
```

All other fields are nullable and null is a valid response type.

## What is the difference between how query fields are executed and mutation fields are executed?

While query fields are executed in parallel, mutation fields run in series, one after the other.

This means that if we send two `incrementCredits` mutations in one request, the first is guaranteed to finish before the second begins, ensuring that we don't end up with a race condition with ourselves.

## What is the special `__typename` field in graphql?

The `__typename` field is used to determine the type of object returned by a query.
This can be helpful for narrowing union types.

## How do you define a custom type in a graphql schema?

Using the syntax `type TYPENAME`

```graphql
type User {
  name: String!
  id: Int
}
```

## Does graphql use semicolons at the end of lines?

No!

```graphql
type User {
  name: String!
  id: Int
}
```

<!--TODO(lukemurray): continue learning with graphql website https://graphql.org/learn/schema/ and graphql spec https://spec.graphql.org/June2018/ -->
