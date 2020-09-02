#!/usr/bin/env python3
import sys
import trm.molly
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Loads a series of spectra that were saved from Molly converts them to JSON format.')
	parser.add_argument('mollyfile', type=str, help='Molly file containing the spectra')
	
	arg = parser.parse_args()
	print(arg)
	
	mollyFilename = arg.mollyfile
	mollyFile = trm.molly.rmolly(mollyFilename)

	sys.exit()		
	for index, r in enumerate(mollyFile):
		wavelengths = []
		flux = []
		fluxErrors = []	
		for f, fe, w in zip(r.f, r.fe, r.wave):
			print(w, f, fe)
			wavelengths.append(w)
			flux.append(f)
			fluxErrors.append(fe)
 
		head = r.head
		spectrum = spectrumClasses.spectrumObject()
		npoints = spectrum.setData(wavelengths, flux, fluxErrors)
		targetName = spectrum.parseHeaderInfo(head)
		spectrum.wavelengthUnits = "\\A"
		spectrum.fluxLabel = r.label
		spectrum.fluxUnits = r.units
		# spectrum.fluxUnits = "relative counts"
		
		print("Parsed headers of %s for HJD: %f"%(targetName, spectrum.HJD))
		spectra.append(spectrum)
		
	numSpectra = len(spectra)

	print("%d spectra loaded."%numSpectra)

	for s in spectra:
		outname = "%s_%f.json"%(s.objectName, s.HJD)
		if arg.suffix!=None:
			outname = "%s_%f_%s.json"%(s.objectName, s.HJD, arg.suffix)
		if hasEphemeris:
			outname = "%s_%f_%s.json"%(s.objectName, ephemeris.getPhase(s.HJD), arg.suffix)
			
		print("Writing to %s"%outname)
		s.writeToJSON(outname)
		
