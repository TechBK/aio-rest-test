/**
 * Created by techbk on 20/03/2016.
 */

import fetch from 'isomorphic-fetch'
const URL = 'http://192.168.145.151:8080'

export function signin(data) {
	return {
		type: 'SIGNUP',
		payload: {
			promise: new Promise((resolve, reject) => {
					setTimeout(() => {
						return fetch(URL+'/users/',{
							method: 'post',
							body: JSON.stringify(data),
							headers: {
								'Accept': 'application/json',
								'Content-Type': 'application/json'
							}
						})
							.then(req => {
								//console.log(req.json())
								return req.json()
							}
							)
							.then(json => {
								if (json.login) return resolve(json)
								else return reject(json)
							})
					}, 1000) // simulate server latency
				}),
			data: data
		}
	}
}

//if (!['john', 'paul', 'george', 'ringo'].includes(values.username)) {
//		reject({username: 'User does not exist', _error: 'Login failed!'});
//	} else if (values.password !== 'redux-form') {
//		reject({password: 'Wrong password', _error: 'Login failed!'});
//	} else {
//		dispatch(showResults(values));
//		resolve();
//	}