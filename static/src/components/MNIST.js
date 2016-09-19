import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as actionCreators from '../actions/auth';

function mapStateToProps(state) {
    return {
        isRegistering: state.auth.isRegistering,
        registerStatusText: state.auth.registerStatusText,
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actionCreators, dispatch);
}

@connect(mapStateToProps, mapDispatchToProps)
class MNIST extends React.Component { // eslint-disable-line react/prefer-stateless-function
    render() {
        return (
            <div className="col-md-8">
                <h1>MNIST</h1>
                <hr />

              <div className="row">
                <div className="col-md-6">
                  <p>draw a digit here!</p>
                  <canvas id="main"></canvas>
                  <p>
                    <button id="clear" className="btn btn-default">clear</button>
                  </p>
                </div>
                <div className="col-md-6">
                  <p>input:</p>
                  <canvas id="input"></canvas>
                  <hr />
                  <p>output:</p>
                  <table id="output" className="table">
                    <tr>
                      <th className="col-md-1"></th>
                      <th className="col-md-2">simple</th>
                      <th className="col-md-2">convolutional</th>
                    </tr>
                    <tr>
                      <th>0</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>1</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>2</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>3</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>4</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>5</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>6</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>7</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>8</th>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <th>9</th>
                      <td></td>
                      <td></td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
        );
    }
}

export default MNIST;
