import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {login} from "./login";

export default NextAuth({
  providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                username: { label: "Username", type: "text", placeholder: "username" },
                password: { label: "Password", type: "password" },
            },
            async authorize(credentials:any, req:any): Promise<any> {
                const data = await login(credentials);
                if (data) {
                    return data;
                } else {
                    return null;
                }
            }
        })
    ],
    pages: {
        "signIn": "/login",
        "signOut": "/logout",
    },
    callbacks: {
        async jwt({token, user}) {
            return{...token, ...user};
        },
        async session({session, token}) {
            session.user = token;
            return session;
        }
    },
});