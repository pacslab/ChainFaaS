/*
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
*/

const shim = require('fabric-shim');
const ClientIdentity = require('fabric-shim').ClientIdentity;
const util = require('util');

var Chaincode = class {

  // Initialize the chaincode
  async Init(stub) {
    console.info('========= monetary Init =========');
    let ret = stub.getFunctionAndParameters();
    console.info(ret);
    let args = ret.params;

    // initialise only if 4 parameters passed.
    // initialise only if 4 parameters passed.
    if (args.length != 4) {
      return shim.error('Incorrect number of arguments. Expecting 4');
    }

    let A = args[0];
    let B = args[2];
    let Aval = args[1];
    let Bval = args[3];

    if (isNaN(parseInt(Aval)) || isNaN(parseInt(Bval))) {
      return shim.error('Expecting integer value for asset holding');
    }

    try {
      await stub.putState(A, Buffer.from(Aval));
      try {
        await stub.putState(B, Buffer.from(Bval));
        return shim.success();
      } catch (err) {
        return shim.error(err);
      }
    } catch (err) {
      return shim.error(err);
    }
  }

  
  async Invoke(stub) {
    console.log("Inside invoke of cc!")
    let ret = stub.getFunctionAndParameters();
    console.info(ret);
    let method = this[ret.fcn];
    if (!method) {
      console.error('no method of name:' + ret.fcn + ' found');
      return shim.error('no method of name: ' + ret.fcn + ' found');
    }

    console.info('\nCalling method : ' + ret.fcn);
    try {
      let payload = await method(stub, ret.params);
      return shim.success(payload);
    } catch (err) {
      console.log(err);
      return shim.error(err);
    }
  }

  async new_user(stub){
    console.info('========= monetary new_user =========');
    let ret = stub.getFunctionAndParameters();
    console.info(ret);
    let args = ret.params;
    if (args.length != 2) {
      throw new Error('Incorrect number of arguments. Expecting 2');
    }

    let A = args[0];
    let Aval = args[1];

    if (isNaN(parseInt(Aval))) {
      throw new Error('Expecting integer value for asset holding');
    }

    let key = await stub.getState(A);
    console.log(key.length)
    if (key.length == 0){
      console.log('User does not exist');
      try {
        await stub.putState(A, Buffer.from(Aval));
      } catch (err) {
        throw new Error(err);
      }
    }
    else{
      console.log('User exists')
      throw new Error('This user already exists')
    }
  }
  
  async move(stub, args) {
    let cid = new ClientIdentity(stub); 
    let requester_username = cid.attrs['hf.EnrollmentID']
    console.log('Move username: ', requester_username)
    
    if (args.length != 3) {
      throw new Error('Incorrect number of arguments. Expecting 3');
    }

    let A = args[0];
    let B = args[1];
    if (!A || !B) {
      throw new Error('asset holding must not be empty');
    }

    // Get the state from the ledger
    let Avalbytes = await stub.getState(A);
    if (!Avalbytes) {
      throw new Error('Failed to get state of asset holder A');
    }
    let Aval = parseInt(Avalbytes.toString());

    let Bvalbytes = await stub.getState(B);
    if (!Bvalbytes) {
      throw new Error('Failed to get state of asset holder B');
    }

    let Bval = parseInt(Bvalbytes.toString());
    // Perform the execution
    let amount = parseInt(args[2]);
    if (isNaN(amount)) {
      throw new Error('Expecting integer value for amount to be transaferred');
    }
    if (Aval < amount) {
      throw new Error('There is not enough money in account A');
    }
      Aval = Aval - amount;
      Bval = Bval + amount;
      console.info(util.format('Aval = %d, Bval = %d\n', Aval, Bval));

      // Write the states back to the ledger
      await stub.putState(A, Buffer.from(Aval.toString()));
      await stub.putState(B, Buffer.from(Bval.toString()));
  }

  // query callback representing the query of a chaincode
  async query(stub, args) {
    if (args.length != 1) {
      throw new Error('Incorrect number of arguments. Expecting name of the person to query')
    }

    let jsonResp = {};
    let A = args[0];

    // Get the state from the ledger
    let Avalbytes = await stub.getState(A);
    if (!Avalbytes) {
      jsonResp.error = 'Failed to get state for ' + A;
      throw new Error(JSON.stringify(jsonResp));
    }

    jsonResp.name = A;
    jsonResp.amount = Avalbytes.toString();
    console.info('Query Response:');
    console.info(jsonResp);
    return Avalbytes;
  }
};

shim.start(new Chaincode());
