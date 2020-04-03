/*
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
*/

const shim = require('fabric-shim');
const ClientIdentity = require('fabric-shim').ClientIdentity;
const util = require('util');
// const request = require('request');
const sync_request = require('sync-request'); 

var Chaincode = class {
    constructor() {    
        this.setTime = this.setTime.bind(this)
        this.receivedResult = this.receivedResult.bind(this)
        this.makePayment = this.makePayment.bind(this)
    }

    // Initialize the chaincode
    async Init(stub) {
        console.info('============= START : Initialize Ledger ===========');
        const jobs = [
            {
                service: '1',
                developer:'11',
                provider: 'Sara',
                provider_org: 'Org1',
                time: '100',
                cost: '1.55',
                received: 'False',
                payment_done: 'False', 
            },
            
        ];

        for (let i = 0; i < jobs.length; i++) {
            jobs[i].docType = 'job';
            try {
                await stub.putState('JOB' + i, Buffer.from(JSON.stringify(jobs[i])));
            } catch (err) {
                return shim.error(err);
            }
            console.info('Added <--> ', jobs[i]);
        }
        console.info('============= END : Initialize Ledger ===========');
        return shim.success();
    }

    async queryJob(stub, args) {
        // aksdfgnsf
        if (args.length != 1) {
            throw new Error('Incorrect number of arguments. Expecting number of the job to query')
        }
        let jsonResp = {};
        let jobNumber = args[0];
        const jobAsBytes = await stub.getState("JOB" + jobNumber); // get the job from chaincode state
        if (!jobAsBytes || jobAsBytes.length === 0) {
            throw new Error(`${jobNumber} does not exist`);
        }
        jsonResp.name = "JOB" + jobNumber;
        jsonResp.amount = jobAsBytes.toString();
        console.info('Query Response:');
        console.info(jsonResp);
        console.info(jobAsBytes.toString())
        console.log(jobAsBytes.toString());
        return jobAsBytes;
    }

    
    async createJob(stub, args) {
        console.info('============= START : Create job ===========');
        
        let cid = new ClientIdentity(stub); 
        let requester_username = cid.attrs['hf.EnrollmentID']
        let requester_affiliation = cid.attrs['hf.Affiliation']
        let controller_username = 'controller'
        let controller_org = 'Org1'

        if (requester_username.toLowerCase() != controller_username || 
            !requester_affiliation.includes(controller_org.toLowerCase())){
            throw new Error("You are not authorized to create a new job.")
        }

        let jobID = args[0];
        let jobAsBytes = await stub.getState("JOB" + jobID);
        if (jobAsBytes && jobAsBytes.length != 0) {
            throw new Error(`Job ${jobID} already exists`);
        }

        let service = args[1];
        let developer = args[2];
        let provider = args[3];
        let provider_org = args[4];
        let time = '0';
        let cost= '0.0';
        const job = {
            service,
            docType: 'job',
            developer,
            provider,
            provider_org,
            time,
            cost,
            received: 'False',
            payment_done: 'False'
        };

        await stub.putState('JOB'+ jobID, Buffer.from(JSON.stringify(job)));
        console.info('============= END : Create job ===========');
    }

    async setTime(stub, args){
        let cid = new ClientIdentity(stub); 
        let requester_username = cid.attrs['hf.EnrollmentID']
        let requester_affiliation = cid.attrs['hf.Affiliation']

        if (args.length != 2) {
            throw new Error('Incorrect number of arguments. Expecting 2');
        }
        let jobID = args[0]
        let jobAsBytes = await stub.getState("JOB" + jobID);
        if (!jobAsBytes || jobAsBytes.length === 0) {
            throw new Error(`Job ${jobID} does not exist`);
        }
        let jobVal = JSON.parse(jobAsBytes.toString());
        console.log('jobval provider: ', jobVal['provider'])
        console.log('requester_username:', requester_username)

        if (jobVal['provider'] != requester_username || 
           !requester_affiliation.includes(jobVal['provider_org'].toLowerCase())){
            throw new Error('You are not authorized to change the time of this job.');
        }

        if (jobVal['time'] != '0'){
            throw new Error("The time for this job is already set and can't be changed.")
        }
        let reported_time = args[1] 
        jobVal['time'] = reported_time;
        jobVal['cost'] = await this.calculateCost(jobVal['time']);

        // Write the states back to the ledger
        await stub.putState("JOB" + jobID, Buffer.from(JSON.stringify(jobVal)));
        console.log(jobVal)
        console.log("Time and cost for this job is set.")

        await this.makePayment(stub, jobID, jobVal);
    }

    async receivedResult(stub, args){
        let cid = new ClientIdentity(stub); 
        let requester_username = cid.attrs['hf.EnrollmentID']
        let requester_affiliation = cid.attrs['hf.Affiliation']
        let controller_username = 'controller'
        let controller_org = 'Org1'

        if (args.length != 1) {
            throw new Error('Incorrect number of arguments. Expecting 1');
        }
        let jobID = args[0]
        let jobAsBytes = await stub.getState("JOB" + jobID);

        if (requester_username != controller_username || 
            !requester_affiliation.includes(controller_org.toLowerCase())){
                throw new Error('You are not authorized to change received status of this job.');
            }

        if (!jobAsBytes || jobAsBytes.length === 0) {
            throw new Error(`Job ${jobID} does not exist`);
        }

        let jobVal = JSON.parse(jobAsBytes.toString());

        if (jobVal['received'] == 'True'){
            throw new Error("The status of this job is already set to received.")
        }

        console.log('requester_username:', requester_username)
        jobVal['received'] = 'True';
        await stub.putState("JOB" + jobID, Buffer.from(JSON.stringify(jobVal)));
        console.log('first jobVal: ', jobVal)
        // Write the states back to the ledger
        console.log("Job updated.")
    }

    async calculateCost(time){
        return String(Number(time) * 0.01)
    }

    async makePayment(stub, jobID, inputVal=null){
        console.log("inside make payment func " + jobID);
        
        if (inputVal == null){
            var jobAsBytes = await stub.getState("JOB" + jobID);
            console.log("Got the state job")
            if (!jobAsBytes || jobAsBytes.length === 0) {
                throw new Error(`Job ${jobID} does not exist`);
            }
            var jobVal = JSON.parse(jobAsBytes.toString());
            console.log('Here is the jobVal: ', jobVal);
        }
        else {
            var jobVal = inputVal;
        }
        if (jobVal['payment_done'] == 'True'){
            console.log("Payment for this job has already been processed.")
            throw new Error("Payment for this job has already been processed.")
        }
        if (jobVal['time'] == '0' || jobVal['received'] == 'False'){
            console.log("One of time or received are not set yet!")
        } else {
            try{
                console.log("just before calling the other chaincode")
                let r = await this.invokeMonetary(stub, jobVal['developer'], jobVal['provider'], jobVal['cost'])
                jobVal['payment_done'] = 'True';
                console.log(jobVal)
                await stub.putState("JOB" + jobID, Buffer.from(JSON.stringify(jobVal)));
            } catch(error){
                console.log('An error occured in the payment. ', error)
                throw new Error(error)
            }
        }    
        await this.sleep(3000);
    }

    sleep(ms) {
        return new Promise((resolve) => {
          setTimeout(resolve, ms);
        });
    }  

    async invokeMonetary(stub, from_account, to_account, amount){
        let monetary_chain = "monetary"
     
        let arg = ["move", from_account, to_account, amount]
        try {
            console.log("Just before calling the other chaincode!")
            let response = await stub.invokeChaincode(monetary_chain, arg, "mychannel")
            console.log(response)
            return response;
        } catch (err) {
            console.log('In invoke monetary catch')
            console.log(err);
            return shim.error(err);
        }

    }

    async Invoke(stub) {
        let ret = stub.getFunctionAndParameters();
        console.info(ret);

        let method = this[ret.fcn];
        if (!method) {
            console.error('no method of name:' + ret.fcn + ' found');
            return shim.error('no method of name:' + ret.fcn + ' found');
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
    
};

shim.start(new Chaincode());
