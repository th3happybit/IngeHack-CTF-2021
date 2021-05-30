import { ApolloServer, gql, MockList } from "apollo-server-micro";
import casual from "casual-browserify";

const typeDefs = gql`
  type Query {
    colors: [Color!]!
    fl4g: [Fl4g!]!
  }
  type Color {
    name: String
    hex: String
  }
  type Fl4g {
    fl4g: String
  }
`;

const mocks = {
  Query: () => ({
    colors: () =>
      new MockList(30, () => ({
        name: casual.color_name,
        hex: casual.rgb_hex,
      })),
  }),
};

const resolvers = {
  Query: {
    fl4g(parent, args, context) {
      return [{ fl4g: "SW5nZUhhY2t7SV9zaDB1bGRfUzNjdXIzX015X0dyNHBoUWxfUzNydjNyXzopKSkpKX0=" }];
    },
  },
};

const apolloServer = new ApolloServer({
  typeDefs,
  resolvers,
  mocks,
  mockEntireSchema: false,
});

export const config = {
  api: {
    bodyParser: false,
  },
};

export default apolloServer.createHandler({
  path: "/api/96b97cfae94f1e5deeb3f086aa34f45e/graphql",
});
