import React from "react";
import ReactDOM from "react-dom";
import App from "next/app";
import Head from "next/head";
import Router from "next/router";

class MyApp extends App {
  componentDidMount() {
    let comment = document.createComment(`IngeHack`);
    document.insertBefore(comment, document.documentElement);
  }
  static async getInitialProps({ Component, router, ctx }) {
    let pageProps = {};

    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }

    return { pageProps };
  }
  render() {
    const { Component, pageProps } = this.props;
    const s3cr3t = "inghack{w33b_d3v_guru}"
    const modifiedProps = {...pageProps, s3cr3t }
    return (
        <React.Fragment>
          <Head>
            <meta
              name="viewport"
              content="width=device-width, initial-scale=1, shrink-to-fit=no"
            />
            <title>Devtools</title>
          </Head>
            <Component {...modifiedProps} />
        </React.Fragment>
    );
  }
}

export default MyApp