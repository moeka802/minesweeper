import React from "react";

import axios from "axios";

export default class Sample extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message1: "",
      message2: "",
    };
  }

  handleClick = () => {
    axios
      .post("http://localhost:8000/", {
        param1: "hoge",
        param2: "fuga",
      })
      .then((res) => {
        this.setState({
          message1: res.data.param1,
          message2: res.data.param2,
        });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  render() {
    return (
      <div>
        <button onClick={this.handleClick}>POST</button>
        <p>メッセージ1 = {this.state.message1}</p>
        <p>メッセージ2 = {this.state.message2}</p>
      </div>
    );
  }
}
