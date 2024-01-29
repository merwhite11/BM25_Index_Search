
var {Horoscope} = require('./index.js')

module.exports = {
  save: (name, sign, day, data) => {
    console.log('horoscope', typeof Horoscope)
    const filter = {
      name: name,
      sign: sign
    }
    const update = {
      name: name,
      sign: sign,
      day: day,
      horoscope: data.description, compatibility: data.compatibility,
      color: data.color,
      luckyNumber: data.lucky_number, luckyTime: data.lucky_time,
      mood: data.mood
    }
    return Horoscope.findOneAndUpdate(filter, update, {
      new: true,
      upsert: true
    })
  },

 find: (zodiac) => {
   return Horoscope.find({sign: zodiac}, 'name')

 }




}
