import pandas as pd
import sys


# Dead simple python script to get the processing attribution from an IF filename.

class BinaryConverter(object):

    @staticmethod
    # Convert the base-10 number to its binary representation as a list, then use list comprehension to convert that
    # into a compact list of indices showing the bits set to true.
    def toBitSet(base10bigInt):
        binRep = [int(i) for i in bin(base10bigInt)[2:]]
        revList = list(reversed(binRep))
        return [i for i in range(len(revList)) if revList[i] > 0]

    @staticmethod
    # Convert base-36 'number' into a base-10 one, and then to a bitset that describes which bits are set to true.
    def toBitSetFromBase36(base36String):
        bigInteger = int(base36String, 36)
        return BinaryConverter.toBitSet(bigInteger)


class VersionOneFileNamer:
    VERSION = "1"

    def getVersion(self):
        return self.VERSION

    def parse_file_name(self, filename):
        return filename.split('_')


class StaticSettings:
    NAME = "mirage-utils"
    DC_BIT_ID = "dcId"
    DEFAULT_ID_VERSION = "1"
    FEATURE_MAP_FILE_VERSION_1 = "featuremap_v1.csv"


class FileNamerFactory:
    versionOne = VersionOneFileNamer()
    id_length = len(StaticSettings.DC_BIT_ID)

    @staticmethod
    def getByVersion(version=None):
        if not version:
            version = StaticSettings.DEFAULT_ID_VERSION
        if version == "1":
            return FileNamerFactory.versionOne
        raise Exception("There is no FileNamer implemented for specified version")

    @staticmethod
    def getByFilename(filename):
        return FileNamerFactory.getByVersion(FileNamerFactory.findVersionFromFilename(filename))

    @staticmethod
    def findVersionFromFilename(filename):
        if StaticSettings.DC_BIT_ID in filename:
            start = filename.index(StaticSettings.DC_BIT_ID) + FileNamerFactory.id_length
            return filename[start: start + 1]
        return None


class ParseFilename(object):
    # The length of the DC image ID identifier.
    ID_LENGTH = None

    def __init__(self):
        self.ID_LENGTH = StaticSettings.DC_BIT_ID

    @staticmethod
    def parse(filename):
        return FileNamerFactory.getByFilename(filename).parse_file_name(filename)


def get_feature_list(processedImageIdLocal):
    encoded_tag = ParseFilename.parse(processedImageIdLocal)[2]
    #print(BinaryConverter.toBitSetFromBase36(encoded_tag))

    data = pd.read_csv(StaticSettings.FEATURE_MAP_FILE_VERSION_1)
    df = pd.DataFrame(data)

    indices = BinaryConverter.toBitSetFromBase36(encoded_tag)

    for index in indices:
        print(df.iloc[index]['feature'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No filename specified.  Using example filename '104001004E9B7800_dcId1_y1u6j5s.tif'...")
        processedImageId = "104001004E9B7800_dcId1_y1u6j5s"
        get_feature_list(processedImageId)
    else:
        processedImageId = sys.argv[1].split('.')[0]  # remove file extension
        get_feature_list(processedImageId)
