# ATK-DEF-MODIFICATION

Source: https://www.masterduelmeta.com/articles/guides/expanded-rule-book#ATK-DEF-MODIFICATION

### Boost!
This information is taken from an article written by YGOrganization.

#### ATK/DEF Modifiers
When modifying the ATK/DEF of a monster, there are 3 things that are checked to determine how it is applied: 
 
 
 Is the value change Additive/Subtractive or setting to a new value? 
 Does the effect activate ? 
 Does it modify current or Original ATK/DEF? 
 Depending on the answers, there are 6 possible ways to apply the modification: 
 
 
 Activated effect modifier that increases/decreases the current ATK/DEF. 
 Non-activated effect modifier that increases/decreases the current ATK/DEF. 
 Activated effect modifier that sets current ATK/DEF to determined value. 
 Non-activated effect modifier that sets current ATK/DEF to determined value. 
 Activated effect modifier that sets original ATK/DEF to determined value. 
 Non-activated effect modifier that sets original ATK/DEF to determined value. 
 Master Duel will handle all of this information for you , but this is helpful to know if you want to know why modifiers work the way they do.

#### Applying any effect that increases or decreases ATK/DEF.
Generally, regardless of what kind of effect was previously applied to a monster, increases/decreases are simply added to the existing value. This is true for both activated effects and non-activated effects. 
 Note that a monster’s ATK/DEF cannot be lower than 0. Decreases are still applied to a monster’s ATK/DEF even if they would become lower than 0, but will be cut off at 0. The leftover amount is still “stored”, so that it needs to be taken into account when you further increase a monster’s ATK/DEF.

##### Example:
The effect of Loading... 
 is applied to Loading... 
 , which reduces its ATK by 800. Since Harpie Girl has an original ATK of 500, its ATK becomes 0. If Loading... 
 is then Summoned, its effect increases the ATK of Harpie Girl by 500. The ATK of Harpie Girl becomes 200, not 500 . Once the effect of Forbidden Lance is no longer applying, Harpie Girl will return to 1000 ATK.

#### Applying an activated effect that sets ATK/DEF to a determined value.
These are activated effects that “halve”, “double”, or “switch” the current ATK/DEF of a monster, or make it “become” a specific value. Despite the variety of words used, they really all mean the same thing. Mechanically, a card like Loading... 
 does not actually double a monster’s ATK, but rather it sets its ATK to a value that is twice its previous ATK. If the effect of Limiter Removal is applied to Loading... 
 ’s 1400 ATK for example, it is making its ATK become 2800. 
 When these effects are applied, they overwrite any previous modifiers , even if they use those modifiers as a reference point to determine the new value (such as halving or doubling a monster’s current ATK), so those previous changes to the current ATK/DEF are not reapplied . These effects essentially lock in or freeze the ATK/DEF at the newly-determined value. 
 If the new effect stops applying after a certain duration, a continuously-applied effect’s modifiers are reapplied. However, changes that were made by previous activated effects to the current ATK/DEF are never reapplied, as they have essentially been erased.

##### Examples:
The effect of Loading... 
 is applied to Loading... 
 , which increases its ATK to 2800. After that, the effect of Loading... 
 is applied to that 7 Colored Fish, so its ATK is halved to 1400 and remains there for the duration of the turn . When the effect of Armored Bee expires, the ATK of 7 Colored Fish will be 1800. The effect of Aqua Jet is NOT reapplied. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 has an original ATK of 3200 from its own effect, and has used its effect that makes it lose 800 ATK three times while on the field (losing a total of 2400 ATK), so its current ATK is 800. If Apollousa, Bow of the Goddess is equipped with Loading... 
 and battles a Loading... 
 , the effect of Moon Mirror Shield activates and sets Apollousa’s ATK to 2200. After damage calculation is over, its ATK returns to its original value of 3200. The 2400 ATK previously lost by its effect is NOT reapplied. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 is equipped with Loading... 
 , so that its ATK/DEF are 3100/2700. If Loading... 
 is activated from the hand, the effect of Mage Power immediately adjusts as a result of Limiter Removal being placed into the Spell & Trap Zone, so the ATK/DEF of Barrel Dragon becomes 3600/3200. When Limiter Removal resolves, it doubles that 3600 ATK to 7200. Afterward, Limiter Removal is sent to the Graveyard, but Barrel Dragon’s ATK remains 7200 . Even if more Spells/Traps are placed on the field, or even if Mage Power is destroyed, the ATK stays at 7200. (Note that Barrel Dragon’s DEF will drop to 2700 after Limiter Removal resolves, and will continue to be affected by Mage Power.) 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 The effect of Loading... 
 is applied to Loading... 
 , and its original ATK becomes 1150. When the effect of Powercode Talker is activated during damage calculation, it sets its ATK to double its original ATK (which is now 1150), so its ATK becomes 2300. After damage calculation, its ATK returns to the value of its original ATK set by Shrink, 1150. Once the turn ends, its original and current ATK return to 2300.

#### Applying a non-activated effect that sets ATK/DEF to a determined value.
These are continuously-applied effects that change ATK/DEF to a specific value . Once these effects are applied, any previous non-activated increases/decreases are reapplied to the ATK/DEF. There are exceptions to this rule that will be explained later.

##### Examples:
Loading... 
 is equipped with Loading... 
 , so its ATK is 500. If Relinquished then activates its effect and equips Loading... 
 , the ATK of Relinquished becomes 2000 (with 1500 DEF), and then the 500 ATK from Black Pendant is reapplied. Its ATK becomes 2500. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 is losing 1000 ATK from its own effect, so its ATK is 1000. If Boar Soldier is equipped with Loading... 
 , its ATK becomes 0 or 3000 . (The effect of Megamorph makes its ATK become 1000 or 4000, but its own effect is reapplied and it loses 1000 ATK.) 
 When these effects are applied, any increases/decreases previously applied by an activated effect, or any changes to a monster’s current ATK/DEF set by an activated effect, will not reapply. However, the old modifiers are only masked and don’t disappear entirely . If the new effect stops applying, the first effect’s modifier will come back into effect.

##### Examples:
The effect of Loading... 
 is applied to Loading... 
 , which increases its ATK to 2600. If Luster Dragon is equipped with Loading... 
 , its ATK/DEF becomes 100 . If Darkworld Shackles is destroyed before the end of this turn, the ATK of Luster Dragon becomes 2600 again until the end of the turn. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 The effect of Loading... 
 is applied to Loading... 
 , which halves its ATK to 950. If Luster Dragon is equipped with Loading... 
 , its ATK/DEF becomes 100. If Darkworld Shackles is destroyed before the end of this turn, the ATK of Luster Dragon becomes 950 again until the end of the turn. 
 When two non-activated effects are applied that each set ATK/DEF to a determined value, whichever effect was applied most recently will take effect. If that new effect then stops applying, the first effect will be reapplied.

##### Example:
Player A has lower Life Points than Player B, and Player A controls a Loading... 
 equipped with their own Loading... 
 , so the ATK of that monster is 4600. If Player B equips their Megamorph to that Goblin Attack Force without any change in LP, its ATK becomes 1150. If Player B’s Megamorph is destroyed, the ATK of Goblin Attack Force returns to 4600 .

#### Applying an activated effect that changes original ATK/DEF.
Effects that change a monster’s original ATK/DEF treat the new value as the original ATK/DEF, as if it were the value printed on the card . When these effects change a monster’s original ATK/DEF, previous increases or decreases are reapplied whether they are activated or non-activated.

##### Example:
Loading... 
 is equipped with Loading... 
 , which increases its ATK to 2500. If the effect of Loading... 
 is applied to Flame Swordsman, its original ATK/DEF becomes 1600/1800, but the effect of Salamandra is reapplied , so its current ATK becomes 2300. 
 When an activated effect changes a monster’s original ATK/DEF, previously-applied activated effects that set the monster’s current ATK/DEF to a determined value are wiped, and not reapplied .

##### Examples:
The effect of Loading... 
 is applied to Loading... 
 , which halves its ATK/DEF to 1200/900. If the effect of Loading... 
 is applied to Black Rose Dragon, its original ATK is halved to 1200, and its current ATK will start over from there , so it remains 1200 as a result. When the effect of Shrink stops applying at the end of the turn, the ATK of Black Rose Dragon returns to 2400 , while its DEF remains 900. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 activates its effect targeting Loading... 
 , and its current ATK/DEF becomes 2500/2100. If the effect of Loading... 
 is applied, the ATK/DEF of Copycat each become 0 . When the turn ends and the effect of Shield & Sword stops applying, the ATK/DEF of Copycat switch again, but its effect is never reapplied . Its ATK/DEF will be 0. 
 If these effects are applied while a non-activated effect is setting ATK/DEF to a determined value, that previous effect is reapplied once the original ATK/DEF is changed.

##### Examples:
Loading... 
 is equipped with Loading... 
 , and its ATK/DEF are each 100. If the effect of Loading... 
 is applied to Il Blud, its original ATK becomes 1050, but the effect of Darkworld Shackles is reapplied and its current ATK remains 100. If Darkworld Shackles is destroyed this turn, its ATK becomes 1050. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 is equipped with Loading... 
 , and its ATK is either 1200 or 4800. If the effect of Loading... 
 is applied to Red-Eyes Black Dragon, its original ATK becomes 1200. The effect of Megamorph is reapplied, but since its effect is determined by the monster’s original ATK , the ATK of Red-Eyes Black Dragon will either be 600 or 2400. 
 When an activated effect changes a monster’s original ATK, any previous changes to the monster’s original ATK are wiped, even if the new original ATK is based on the old (modified) original ATK. This is important if the old change was permanent, but the new one is temporary.

##### Example:
The effect of Loading... 
 is applied to Loading... 
 , so the original ATK of Clear Wing Synchro Dragon becomes 1250 indefinitely . If the effect of Loading... 
 is applied to that Clear Wing Synchro Dragon, its original ATK becomes 625 . When the turn ends and the effect of Shrink stops applying, the original ATK of Clear Wing Synchro Dragon becomes 2500 .

#### Applying a non-activated effect that changes original ATK/DEF.
As with the activated effects that change original ATK/DEF, previous increases or decreases are reapplied.

##### Example:
An Loading... 
 gained 3000 ATK from its own effect. If it is equipped with Loading... 
 , its original ATK becomes 1000 or 2400 , but the boost from its own effect is reapplied , so its current ATK will be 4000 or 5400 . 
 Previous changes that result from an activated effect setting a monster’s current ATK/DEF will remain active , so that the current ATK/DEF of the monster does not change even though the original ATK/DEF may change “behind the scenes”.

##### Examples:
Loading... 
 halves its ATK with its own effect. If Drill Warrior is equipped with Loading... 
 and attacks an opponent’s monster, its current ATK remains 1200 , even though its original ATK becomes 4800. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 The effect of Loading... 
 is applied to Loading... 
 , halving its ATK to 800. If Loading... 
 is activated, Fire Hand’s original ATK and DEF switch, but its current ATK remains 800 . Its original (and current) DEF becomes 1600. 
 Similarly, if a monster is already being affected by a non-activated effect that sets its current ATK/DEF to a determined value, and then its original ATK is changed by a non-activated effect, the current ATK/DEF does not change even though the original does.

##### Example:
Loading... 
 is equipped with Loading... 
 , so its ATK/DEF are each 100. If it is then equipped with Loading... 
 , its original ATK becomes 2400, but its current ATK and DEF remain 100 . 
 If the monster’s original ATK/DEF was previously changed by an activated effect , the non-activated effect changing its original ATK/DEF will apply.

##### Example:
The effect of Loading... 
 is applied to Loading... 
 , and its original ATK becomes 1750. If Ultimate Conductor Tyranno is equipped with Loading... 
 , its original ATK becomes 1000 or 2400 . If Unstable Evolution is destroyed before the end of the turn , the ATK of Ultimate Conductor Tyranno returns to 1750.

#### Exceptions – Applying a special non-activated effect that is always applied last.
As mentioned previously, certain effects that set a monster’s current ATK/DEF continuously are always reapplied last as new modifiers are introduced, breaking some of the rules established above . Even though they can be described in the same way – non-activated effects that set ATK/DEF to a determined value – they sometimes just work differently. 
 Firstly, we'll go over the effects that halve, double, or switch a monster’s current ATK/DEF continuously, since these have no counterparts to anything metioned previously, making them easier to categorize. 
 Also mentioned above, activated effects such as Loading... 
 don’t truly double a monster’s ATK ; they set a monster’s ATK to a value that is twice its previous ATK, and “freeze” it. The same is true with cards like Loading... 
 , which switch a monster’s current ATK/DEF. The special effects discussed in this section actually do double, halve, or switch ATK/DEF , and any new modifiers are applied to the previous level of modification, but the special effect is then reapplied to the new total.

##### Examples:
Loading... 
 and Loading... 
 are on the field. The effect of Super Crashbug switches the ATK/DEF of Number 17: Leviathan Dragon, to be 0/2000. If the effect of Number 17: Leviathan Dragon is activated, its ATK is recalculated with the effect of Super Crashbug being applied last. The ATK/DEF becomes 0/2500, not 500/2000. If Super Crashbug leaves the field , the ATK/DEF becomes 2500/0. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 attacks while Loading... 
 is on the field. Once the attack is declared, the ATK of Injection Fairy Lily is halved to 200 . During damage calculation, if the effect of Injection Fairy Lily is activated, its ATK is recalculated . After its effect resolves, its ATK becomes 1700, which is 3400 halved. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 is equipped with Loading... 
 , and Loading... 
 is on the field, which halves the current ATK/DEF of all other monsters on the field. The ATK of Red-Eyes Black Dragon is either 600 or 2400, while its DEF is 1000. 
 Things get more complicated with activated effects that set ATK/DEF to a determined value applied while these special effects are applying . It was previously mentioned that when an effect like Loading... 
 or Loading... 
 resolves, any previous non-activated modification cannot be reapplied . However, cards like Mirror Wall and The Wicked Dreadroot will reapply.

##### Examples:
The effect of Loading... 
 is applied to a Loading... 
 that attacked, so its ATK becomes 1200. If the effect of Cybernetic Magician is then activated, applying to itself, its ATK becomes 2000 , but the effect of Mirror Wall immediately reapplies and halves that amount, so the ATK actually becomes 1000. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 and Loading... 
 are on the field. If Loading... 
 is Normal Summoned, the effect of The Wicked Dreadroot is immediately applied , so the ATK/DEF of Aleister the Invoker becomes 500/900. The effect of Black Garden then activates, and halves the ATK of Aleister the Invoker to 250. Now, the effect of The Wicked Dreadroot is reapplied to the newly-determined value , and halves it further to 125. (The DEF remains 900.) If The Wicked Dreadroot leaves the field, the ATK of Aleister the Invoker becomes 250 again. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Lastly, we have the effects that continuously set a monster’s ATK/DEF to a specific value rather than halve, double, or switch it. As with the cards above, these are always applied last and supersede virtually all other effects that would modify ATK/DEF. 
 While their effects are applying, they (or the monsters their effects are applied to) are effectively immune to any ATK/DEF modifications. One thing to keep in mind again however, is that because they apply continuously, they simply mask the previously-applied modifiers rather than remove them entirely. If the new effect stops applying, the old effects are reapplied .

##### Examples:
Loading... 
 , Loading... 
 , and Loading... 
 are all on the field, and the ATK of Apple Magician Girl is 0 due to the effect of Water Dragon. If Loading... 
 is activated, targeting Apple Magician Girl, its ATK becomes 3000, but the effect of Water Dragon is immediately reapplied and makes the ATK become 0 again. If Water Dragon is destroyed this turn, the ATK of Apple Magician Girl becomes 3000 again. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If Loading... 
 attacks Loading... 
 , Clear Vice Dragon will have 4800 ATK during damage calculation. If Loading... 
 is activated during damage calculation, the ATK of Clear Vice Dragon becomes 2400, but the effect is reapplied and becomes 4800 again. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 and Loading... 
 are on the field, and the ATK/DEF of The Wicked Avatar are each 2400. If the effect of Salamangreat Heatleo is activated, targeting a Loading... 
 in the Graveyard and The Wicked Avatar on the field, the ATK of The Wicked Avatar becomes 1900, but immediately reverts to 2400 . During this turn, if the effects of The Wicked Avatar are negated, its ATK will become 1900 again and its DEF becomes 0 . 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 and an "Option Token" are on the field. The Pendulum Effect of Loading... 
 is applied to the Option Token, which switches its ATK/DEF from 1200/1000 to 1000/1200. However, its ATK/DEF immediately readjusts to be the same as Victory Viper XX03, so they become 1200/1000 again.

#### Exceptions – Activated effects that work like non-activated effects, and vice versa.
A monster’s effect that sets its own current or original ATK/DEF upon being Summoned is generally considered a Continuous Effect , because it does not activate. However, these effects behave more like activated effects with respect to the interaction rules covered above. They are only applied once when the Summon is successful, and are not continuously-applying thereafter. Loading... 
 is similar as well, although its effect is not applied upon being Summoned.

##### Examples:
Loading... 
 has an original ATK of 3200 by its own effect, and has used its effect to decrease its ATK by 800 twice, for a total decrease of 1600 ATK. If the effect of Loading... 
 is applied to Apollousa, Bow of the Goddess, its original ATK becomes 1600 , and the decrease of 1600 by its own effect is reapplied, making its current ATK 0 . At the end of the turn, the original ATK of Apollousa, Bow of the Goddess becomes 0 . 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 Loading... 
 has its ATK/DEF halved by the effect of Loading... 
 , so its ATK/DEF are 200/900. If Loading... 
 is activated, the effect of Naturia Beetle is applied and its original ATK/DEF switch . Its current ATK/DEF will be 1800/400, meaning the effect of Blackwing – Gale the Whirlwind is no longer applied . 
 In the above examples, although the first effect of Loading... 
 and the effect of Loading... 
 are Continuous Effects, they behave more like previously-applied activated effects that change original ATK. (They are closer to something like Loading... 
 than Loading... 
 .) 
 Conversely, there are activated effects that behave like non-activated effects , such as Loading... 
 and Loading... 
 . The activated effect’s resolution is to begin applying a non-activated effect , which then takes effect for a certain amount of time . These cards have effects that activate and resolve, but the applied increase functions like a non-activated effect.

##### Example:
The effect of your Loading... 
 has activated and resolved. Your Loading... 
 with 3700 ATK attacks an opponent’s Defense Position Loading... 
 , and during damage calculation the effect of Kazejin is activated. The ATK of Ritual Beast Ulti-Gaiapelio becomes 0 , and damage calculation occurs with that value . After damage calculation concludes, the effect of Kazejin stops applying and the effect of Spiritual Beast Apelio reapplies, so the ATK of Ritual Beast Ulti-Gaiapelio becomes 3700 .
