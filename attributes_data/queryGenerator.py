


all_prefixes = """
prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
prefix lio: <http://purl.org/net/lio#>
prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
prefix obo: <http://purl.obolibrary.org/obo/>

prefix ho: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/HairOntology/>
prefix img: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/>
prefix frma: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/FRMA/>
prefix mlmo: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
prefix pfd: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/>
prefix wt: <https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/WearableThingsOntology/>

"""

all_missclassified_intro_2 = """
where {
"""

all_misclassified_generic_intro = """
  ## calculates [lowercase_name] Missclassification
  {
    select ?ResultSet (count(?classification) as ?[lowercase_name]Miss)
    where {
      ?ResultSet a mlmo:ResultSet .
      ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
      ?Result mlmo:hasFeature ?Image .

      ?Image lio:depicts ?Person .
"""

johnny_depp_generic_intro = """
  ## calculates how many instances of [lowercase_name] are associated with the person
  {
    select ?ResultSet (count(?classification) as ?[lowercase_name]Count)
    where {
      ?ResultSet a mlmo:ResultSet .
      ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
      ?Result mlmo:hasFeature ?Image .

      ?Image lio:depicts ?Person .
"""

all_misclassified_generic_ending = """
      ?Person fibo-fnd-aap-a:hasName ?Name .
      optional{
       ?Result lcc-lr:hasTag ?classification .
       filter (?classification != ?Name)
      }
    }
    group by ?ResultSet
  }
"""

johnny_depp_generic_ending = """
      optional{
        ?Person fibo-fnd-aap-a:hasName "[person_name]"^^xsd:string .
        filter (?classification = "[person_name]"^^xsd:string) # This line ensures we only have counts for correctly classified images
        ?Result lcc-lr:hasTag ?classification .
      }
    }
    group by ?ResultSet
  }
"""

johnny_depp_generic_model_tagged_ending = """
      optional{
        ?Result lcc-lr:hasTag "[person_name]"^^xsd:string .
        ?Result lcc-lr:hasTag ?classification .
      }
    }
    group by ?ResultSet
  }
"""

johnny_depp_ending = """
}
"""

all_misclassified_ending = """
  # Calulates the total number of incorrect Images
  {
    select ?ResultSet (count(distinct ?Result) as ?totalMiss)
    where {
      ?ResultSet a mlmo:ResultSet .
      ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
      ?Result mlmo:hasFeature ?Image .
      ?Image lio:depicts ?Person .
      ?Person fibo-fnd-aap-a:hasName ?Name

      optional{
       ?Result lcc-lr:hasTag ?classification .
       filter (?classification != ?Name)
      }

    }
    group by ?ResultSet
  }
}
"""



def generate_misclassified_attributes(attributes):
	# attributes is a list of tuples:
	#[  (lowercase_name, [hierarchy way to get to it from Person])  ]
	output_text = all_prefixes

	# then generate all the results that we're finding for the header of the query
	#select ?ResultSet ((?sideburnMiss/?totalMiss)*100 as ?sideburn_missclass_rate) ((?mustacheMiss/?totalMiss)*100 as ?mustache_missclass_rate)
	all_results_list = []
	for a in attributes:
		name = a[0].lower()
		t = "((?" + str(name) + "Miss/?totalMiss)*100 as ?" + str(name) + "_missclass_rate)"
		all_results_list.append(t)
	all_results = "select ?ResultSet " + " ".join(all_results_list)
	output_text += all_results

	# then add the second intro text
	output_text += all_missclassified_intro_2

	# then loop over all the attributes adding the attributes in
	for a in attributes:
		name = a[0].lower()
		a_text = all_misclassified_generic_intro.replace("[lowercase_name]", name)
		for hierarchy in a[1]:
			# loop through the way to get to the attribute adding it to the text:
			a_text += "      " + hierarchy + "\n"
		a_text += all_misclassified_generic_ending
		output_text += a_text

	output_text += all_misclassified_ending
	return output_text

def generate_johnny_depp(attributes, person_name, use_all_images_tagged = False):
	# attributes is a list of tuples:
	#[  (lowercase_name, [hierarchy way to get to it from Person])  ]
	output_text = all_prefixes

	# then generate all the results that we're finding for the header of the query
	#select ?ResultSet ((?sideburnMiss/?totalMiss)*100 as ?sideburn_missclass_rate) ((?mustacheMiss/?totalMiss)*100 as ?mustache_missclass_rate)
	all_results_list = []
	for a in attributes:
		feature = a[0].lower()
		t = "?" + str(feature) + "Count"
		all_results_list.append(t)
	all_results = "select ?ResultSet " + " ".join(all_results_list)
	output_text += all_results

	# then add the second intro text
	output_text += all_missclassified_intro_2

	# then loop over all the attributes adding the attributes in
	for a in attributes:
		feature = a[0].lower()
		a_text = johnny_depp_generic_intro.replace("[lowercase_name]", feature)
		for hierarchy in a[1]:
			# loop through the way to get to the attribute adding it to the text:
			a_text += "      " + hierarchy + "\n"
		if use_all_images_tagged:
			a_text += johnny_depp_generic_model_tagged_ending.replace("[person_name]", person_name)
		else:
			a_text += johnny_depp_generic_ending.replace("[person_name]", person_name)
		output_text += a_text

	output_text += johnny_depp_ending
	return output_text

if __name__ == "__main__":
	

	# all attributes:
	all_attributes = [
		("sideburn", ["?Person obo:BFO_0000051 ?facialHair .", "?facialHair a ho:Sideburn ."]),
		("mustache", ["?Person obo:BFO_0000051 ?facialHair .", "?facialHair a ho:Mustache ."]),
		("FiveOClockShadow", ["?Person obo:BFO_0000051 ?facialHair .", "?facialHair a ho:FiveOClockShadow ."]),
		("Goatee", ["?Person obo:BFO_0000051 ?facialHair .", "?facialHair a ho:Goatee ."]),
		
		("White", ["?Person pfd:hasDemographic ?ethnicity .", "?ethnicity a pfd:White ."]),
		("Asian", ["?Person pfd:hasDemographic ?ethnicity .", "?ethnicity a pfd:Asian ."]),
		("Black", ["?Person pfd:hasDemographic ?ethnicity .", "?ethnicity a pfd:Black ."]),
		("Indian", ["?Person pfd:hasDemographic ?ethnicity .", "?ethnicity a pfd:Indian ."]),
		("StrongNoseMouthLines", ["?Person pfd:hasStrongNoseMouthLines True ."]),
		("NoStrongNoseMouthLines", ["?Person pfd:hasStrongNoseMouthLines False ."]),
		("IsAttractive", ["?Person pfd:isAttractive True ."]),
		("NotIsAttractive", ["?Person pfd:isAttractive False ."]),
		("Masculine", ["?Person pfd:hasDemographic ?genderExpression .", "?genderExpression a pfd:Masculine ."]),
		("Feminine", ["?Person pfd:hasDemographic ?genderExpression .", "?genderExpression a pfd:Feminine ."]),

		("Baby", ["?Person pfd:hasDemographic ?ageRange .", "?ageRange a pfd:Baby ."]),
		("Child", ["?Person pfd:hasDemographic ?ageRange .", "?ageRange a pfd:Child ."]),
		("Youth", ["?Person pfd:hasDemographic ?ageRange .", "?ageRange a pfd:Youth ."]),
		("MiddleAged", ["?Person pfd:hasDemographic ?ageRange .", "?ageRange a pfd:MiddleAged ."]),
		("Senior", ["?Person pfd:hasDemographic ?ageRange .", "?ageRange a pfd:Senior ."]),

		("Chubby", ["?Person pfd:hasDemographic ?weightRange .", "?weightRange a pfd:Chubby ."]),
		("Skinny", ["?Person pfd:hasDemographic ?weightRange .", "?weightRange a pfd:Skinny ."]),
		("BrownEye", ["?Person obo:BFO_0000051 ?face .", "?face obo:BFO_0000051 ?eye .", "?eye a obo:UBERON_0000970 .", "?eye pfd:hasColor ?eyeColor .", "?eyeColor a pfd:Brown."]),
		("Eyeglasses", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Eyeglasses ."]),
		("Sunglasses", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Sunglasses ."]),
		("Earrings", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Earrings ."]),
		("Hat", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Hat ."]),
		("Lipstick", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Lipstick ."]),
		("NeckTie", ["?Person wt:isWearing ?wearable .", "?wearable a wt:NeckTie ."]),
		("Necklace", ["?Person wt:isWearing ?wearable .", "?wearable a wt:Necklace ."]),
		("Bald", ["?Person obo:BFO_0000051 ?headhair .", "?headhair a ho:HeadHair .", "?headhair ho:hasHaircut ?haircut .", "?haircut a ho:Bald ."]),
		("Bangs", ["?Person obo:BFO_0000051 ?headhair .", "?headhair a ho:HeadHair .", "?headhair ho:hasHaircut ?haircut .", "?haircut a ho:Bangs ."]),
		
		("BalancedLightingVariation", ["?Image img:lightingDescribedBy ?lightingDescription .", "?lightingDescription a img:BalancedLightingVariation ."]),
		("HarshLightingVariation", ["?Image img:lightingDescribedBy ?lightingDescription .", "?lightingDescription a img:HarshLightingVariation ."]),
		("SoftLightingVariation", ["?Image img:lightingDescribedBy ?lightingDescription .", "?lightingDescription a img:SoftLightingVariation ."]),

		("BlurryImageFidelity", ["?Image img:fidelityDescribedBy ?imageFidelity .", "?imageFidelity a img:BlurryImageFidelity ."]),
		("SharpImageFidelity", ["?Image img:fidelityDescribedBy ?imageFidelity .", "?imageFidelity a img:SharpImageFidelity ."]),

		]

	# uncomment this to generate the query for all misclassified attributes:
	print(generate_misclassified_attributes(all_attributes))


	# uncomment this to generate the query for Johnny Depp:
	# print(generate_johnny_depp(all_attributes, "George W Bush", True))