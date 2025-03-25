---
title: 2 Ways to Write Easily Testable React Components
date: '2020-08-10T23:46:37.121Z'
layout: post
---

Unit testing my React components is a skill that did not come very easily to me. When working on personal projects, it was so easy to justify not writing unit tests for reasons like the project wasn't very big or I wasn't anticipating having very many users. However, I've recently learned some useful patterns that have made unit testing my components much easier, and now I'm at the point where I even enjoy writing unit tests! These days, I don't write unit tests because I "have to" - I write them because I want to and sleep a lot better at night knowing that my code is protected. I'm going to describe a couple of common patterns that make writing testable components easier.

## How I used to write unit tests

Before I understood too much about test-driven development (TDD), I would spend a few days writing a component and then come back to test it. The problem with this approach was that I would write components that were very difficult to test. Let's take a simple example. Here's a component that fetches a list of users from some API and displays them in a table.

```js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserTable = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios
      .get('https://jsonplaceholder.typicode.com/users')
      .then(({ data }) => setUsers(data));
  }, []);

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map(({ name, username, email }) => (
            <tr key={username}>
              <td>{name}</td>
              <td>{username}</td>
              <td>{email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;
```

Now let's write a unit test for this component. When writing unit tests, we want to think about what the business logic is. So, what does this component do? We see that it fetches a list of users using `axios` in the `useEffect` at the beginning of the functional component, then displays that list of users. Let's write a test that makes sure the component successfully fetches and displays a list of users. Here's what a test might look like:

```js
import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import UserTable from './UserTable';
import axios from 'axios';

describe('UserTable test', () => {
  const mockUsers = [
    {
      name: 'Harry Potter',
      username: 'boywholived',
      email: 'harry@hogwarts.com',
    },
    {
      name: 'Tom Riddle',
      username: 'darklord',
      email: 'voldemort@deatheaters.com',
    },
  ];

  beforeEach(async () => {
    axios.get = jest.fn().mockResolvedValue({ data: mockUsers });
    render(<UserTable />);
    await waitFor(() => expect(axios.get).toHaveBeenCalled());
  });

  test('renders user list', async () => {
    const { getByText } = screen;

    mockUsers.forEach(({ name, username, email }) => {
      expect(getByText(name)).toBeDefined();
      expect(getByText(username)).toBeDefined();
      expect(getByText(email)).toBeDefined();
    });
  });
});
```

Since we don't want to actually make a network request in our unit test, we first mock out the `get` function on `axios` in the `beforeEach` function. That way, when the component is rendered in our test, `axios.get` will return our array of `mockUsers` instead of making a real request. Then in our test, we check that the name, username, and email of each of our mock users is indeed rendered.

This component is pretty straightforward to test, but I find a few problems with it. First of all, there's a decent amount of setup. We have to mock `axios` and then wait for its `get` method to be called (even though our mocked `get` function immediately resolves, it's still asynchronous. We have to wait for the promise to resolve before we can reliably test that the data is rendered). I don't really want to have to worry about the implementation details of the components I'm testing. I could have `axios` calls in many different components, and then I would have to mock it out in every single one of my test files. What if I decided to start using some other fetching library instead of `axios`? Then I would have to change all my tests to mock that new library instead. This is all distracting from the purpose of unit tests - to test the business logic of your components.

I've used a couple of different approaches to solving these problems. The first is dependency injection, and the second is using presentational components.

## Dependency Injection

One of the problems we mentioned with this component is its hard dependency on `axios`. That means we have to worry about mocking `axios` specifically in every component we test that uses it. What if instead of mocking it, we created another component and passed in a `fetchUsers` function as a prop? Then we wouldn't have to mock anything, we could just pass in our own function in the test file. Here's a new version of the component:

```js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const UserTable = ({ fetchUsers }) => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers().then(setUsers);
  }, [fetchUsers]);

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map(({ name, username, email }) => (
            <tr key={username}>
              <td>{name}</td>
              <td>{username}</td>
              <td>{email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const UserTableContainer = () => {
  const fetchUsers = async () => {
    const { data } = await axios.get(
      'https://jsonplaceholder.typicode.com/users'
    );
    return data;
  };

  return <UserTable fetchUsers={fetchUsers} />;
};

export default UserTableContainer;
```

Notice that now we have two components. `UserTable` is a lot like the old component, except it accepts a `fetchUsers` function as a prop. Notice that in the `useEffect`, `fetchUsers` directly assigns `users` to its resolved value. Compare that with how we previously had to extract `data` from the `axios` call. `fetchUsers` is completely generic - it just has to be a function that directly resolves to the array of users to be displayed.

We also have a `UserTableContainer`, which does the heavy lifting of passing in the `fetchUsers` function, which basically just wraps an `axios` call. Now take a look at our revised unit test:

```js
import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import { UserTable } from './App';

describe('UserTable test', () => {
  const mockUsers = [
    {
      name: 'Harry Potter',
      username: 'boywholived',
      email: 'harry@hogwarts.com',
    },
    {
      name: 'Tom Riddle',
      username: 'darklord',
      email: 'voldemort@deatheaters.com',
    },
  ];

  beforeEach(async () => {
    const fetchUsers = jest.fn().mockResolvedValue(mockUsers);
    render(<UserTable fetchUsers={fetchUsers} />);
    await waitFor(() => expect(fetchUsers).toHaveBeenCalled());
  });

  test('renders user list', async () => {
    const { getByText } = screen;

    mockUsers.forEach(({ name, username, email }) => {
      expect(getByText(name)).toBeDefined();
      expect(getByText(username)).toBeDefined();
      expect(getByText(email)).toBeDefined();
    });
  });
});
```

Notice that we are testing `UserTable` instead of `UserTableContainer`. That's because `UserTable` actually contains the logic we want to test - displaying the list of users. This is better because we don't have to mock `axios`. In fact, we no longer care what fetching library our app uses. Notice that in the previous unit test, we had to mock `axios`'s behavior of resolving to an object containing a `data` attribute with the fetched data. We had to know about this in our unit test, but now it really doesn't matter how our fetching library behaves. It's `UserTableContainer`'s job to pass in the `fetchUsers` function, but we don't have to test that because its only job is to provide that function.

This is called dependency injection. `UserTable` asks for the function it will use to fetch the list of users instead of having a hard dependency on `axios`, and consequently it's much easier to test.

This is just one solution to the problems we were having earlier. The other solution I'll discuss is called presentational components.

## Presentational Components

Presentational components are components that only present data, they have no state. For this example, instead of passing in a `fetchUsers` function, we could just make a component that accepts `users` as a prop and displays them. Then we wouldn't have to pass in a `fetchUsers` function at all in our test, all we would have to do is pass in a mock array of users and make sure that the component renders them. Here's the component rewritten to use this approach:

```js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const UserTable = ({ users }) => (
  <div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        {users.map(({ name, username, email }) => (
          <tr key={username}>
            <td>{name}</td>
            <td>{username}</td>
            <td>{email}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

const UserTableContainer = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios
      .get('https://jsonplaceholder.typicode.com/users')
      .then(({ data }) => setUsers(data));
  }, []);

  return <UserTable users={users} />;
};

export default UserTableContainer;
```

Now in our test, we don't even have to wait for anything in our `beforeEach` function. We can just render `UserTable` with the mock users and test that everything is displayed properly.

```js
import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import { UserTable } from './App';

describe('UserTable test', () => {
  const mockUsers = [
    {
      name: 'Harry Potter',
      username: 'boywholived',
      email: 'harry@hogwarts.com',
    },
    {
      name: 'Tom Riddle',
      username: 'darklord',
      email: 'voldemort@deatheaters.com',
    },
  ];

  beforeEach(async () => {
    render(<UserTable users={mockUsers} />);
  });

  test('renders user list', async () => {
    const { getByText } = screen;

    mockUsers.forEach(({ name, username, email }) => {
      expect(getByText(name)).toBeDefined();
      expect(getByText(username)).toBeDefined();
      expect(getByText(email)).toBeDefined();
    });
  });
});
```

Now if that isn't easy to test, I don't know what is!

## Conclusion

Jest's mocking feature is incredibly powerful and useful, but personally I try to avoid it whenever possible. I usually find that I can refactor my components to use either dependency injection or presentation components, and then I don't have to worry about the implementation of my dependencies.

So which of these two approaches to improving your tests is better? It depends. For this simple example, I would probably go with a presentational component because I just want to test that it presents the data correctly. But sometimes I want to test a little more than just presentation, and that's when dependency injection comes in handy. For example, I recently wrote a component that uses `localStorage`. I originally tried mocking it with Jest and it was a huge pain. But after I refactored my component to accept a `storageService`, I was able to test the component easily. In my app, I passed in `localStorage` as the `storageService`, but in my test I passed in an object that looked like `localStorage` but wouldn't actually try to store anything in the browser.

I've found that it's hard to write a hard list of rules for what approach to use in every instance. As I've spent more time writing components and unit tests, I've developed a feel for what makes the most sense. Unit testing isn't just something you do - it's a way of thinking. Being a good unit tester doesn't mean you figure out clever ways to test every component - a huge part is knowing how to write and refactor your code such that it's easy to test in the first place.

Hopefully this has helped you write easier-to-test components! Good luck!
